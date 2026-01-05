from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.database import SessionLocal
from app.models import Company, PlanTier, Product, Category, Order, OrderStatus, PaymentStatus
from datetime import datetime
import uuid
import pytest

client = TestClient(app)

def setup_saas_scenario():
    """Helper para criar ambiente de teste limpo"""
    unique_slug = f"saas-scen-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    
    # 1. Criar Empresa FREE
    company = Company(
        name="Startup Food",
        slug=unique_slug,
        owner_email=f"ceo-{unique_slug}@test.com",
        plan_tier=PlanTier.FREE,
        stripe_customer_id=f"cus_{uuid.uuid4().hex[:8]}"
    )
    db.add(company)
    db.commit()
    
    # 2. Criar Categoria
    category = Category(company_id=company.id, name="Geral")
    db.add(category)
    db.commit()
    
    company_id = str(company.id)
    cat_id = category.id
    
    # 3. Gerar Token de Acesso
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    
    db.close()
    
    return company_id, cat_id, token, unique_slug

def test_full_saas_lifecycle_enforcement():
    """
    TESTE DE INTEGRAÇÃO CRÍTICO:
    Valida se o pagamento no Stripe realmente desbloqueia os limites do sistema.
    
    Fluxo:
    1. Empresa FREE atinge limite de produtos (15).
    2. Tenta criar o 16º -> Falha (402).
    3. Simula Webhook de Pagamento Stripe (Upgrade).
    4. Tenta criar o 16º -> Sucesso (201).
    5. Simula Webhook de Cancelamento Stripe (Downgrade).
    6. Tenta criar o 17º -> Falha (402).
    """
    
    company_id, cat_id, token, slug = setup_saas_scenario()
    headers = {"Authorization": f"Bearer {token}"}
    
    # --- FASE 1: Atingir Limites (FREE) ---
    db = SessionLocal()
    for i in range(15):
        p = Product(category_id=cat_id, name=f"Prod {i}", price=10.0)
        db.add(p)
    db.commit()
    db.close()
    
    # Tentar criar o 16º (Deve falhar)
    payload = {"category_id": cat_id, "name": "Prod 16 Blocked", "price": 20.0}
    res_fail = client.post("/api/admin/menu/products", headers=headers, json=payload)
    assert res_fail.status_code == 402
    assert "Limite do Plano Grátis" in res_fail.json()["detail"]
    
    # --- FASE 2: Upgrade via Webhook (PRO) ---
    mock_checkout_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": {"company_id": company_id},
                "subscription": "sub_premium_123"
            }
        }
    }
    
    with patch("app.services.stripe_service.StripeService.construct_event", return_value=mock_checkout_event):
        webhook_res = client.post("/api/webhooks/stripe", json=mock_checkout_event, headers={"stripe-signature": "ok"})
        assert webhook_res.status_code == 200
        
    # Validar mudança no banco
    db = SessionLocal()
    company = db.query(Company).filter(Company.id == company_id).first()
    assert company.plan_tier == PlanTier.PRO
    db.close()
    
    # Tentar criar o 16º (Deve passar agora)
    res_success = client.post("/api/admin/menu/products", headers=headers, json=payload)
    assert res_success.status_code == 201
    assert res_success.json()["name"] == "Prod 16 Blocked"
    
    # --- FASE 3: Downgrade via Webhook (Cancelamento) ---
    mock_cancel_event = {
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "id": "sub_premium_123", # Mesmo ID da assinatura criada
                "status": "canceled"
            }
        }
    }
    
    with patch("app.services.stripe_service.StripeService.construct_event", return_value=mock_cancel_event):
        webhook_res = client.post("/api/webhooks/stripe", json=mock_cancel_event, headers={"stripe-signature": "ok"})
        assert webhook_res.status_code == 200
        
    # Tentar criar o 17º (Deve falhar novamente, pois voltou a ser FREE e já tem >15 produtos)
    payload_17 = {"category_id": cat_id, "name": "Prod 17 Blocked", "price": 20.0}
    res_fail_again = client.post("/api/admin/menu/products", headers=headers, json=payload_17)
    assert res_fail_again.status_code == 402
    assert "Limite do Plano Grátis" in res_fail_again.json()["detail"]