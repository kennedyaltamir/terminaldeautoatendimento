from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.database import SessionLocal
from app.models import Company, PlanTier
import uuid

client = TestClient(app)

def test_full_subscription_lifecycle():
    """
    Testa o ciclo completo de vida da assinatura:
    1. Cria empresa (Free).
    2. Simula pagamento (Webhook -> Pro).
    3. Simula falha/cancelamento (Webhook -> Free).
    """
    
    # SETUP
    unique_slug = f"saas-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="SaaS Cycle Corp",
        slug=unique_slug,
        owner_email=f"ceo-{unique_slug}@test.com",
        plan_tier=PlanTier.FREE
    )
    db.add(company)
    db.commit()
    company_id = str(company.id)
    db.close()

    # 1. UPGRADE (Simulação de Webhook)
    mock_success_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": {"company_id": company_id},
                "subscription": "sub_active_123"
            }
        }
    }

    with patch("app.services.stripe_service.StripeService.handle_webhook", return_value=mock_success_event):
        res = client.post("/api/webhooks/stripe", json=mock_success_event, headers={"stripe-signature": "ok"})
        assert res.status_code == 200

    # Validação 1: Empresa deve ser PRO
    db = SessionLocal()
    company = db.query(Company).filter(Company.id == company_id).first()
    assert company.plan_tier == PlanTier.PRO
    assert company.stripe_subscription_id == "sub_active_123"
    assert company.subscription_status == "active"
    db.close()

    # 2. DOWNGRADE (Simulação de Cancelamento)
    mock_cancel_event = {
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "id": "sub_active_123",
                "status": "canceled"
            }
        }
    }

    with patch("app.services.stripe_service.StripeService.handle_webhook", return_value=mock_cancel_event):
        res = client.post("/api/webhooks/stripe", json=mock_cancel_event, headers={"stripe-signature": "ok"})
        assert res.status_code == 200

    # Validação 2: Empresa deve voltar a ser FREE
    db = SessionLocal()
    company = db.query(Company).filter(Company.id == company_id).first()
    assert company.plan_tier == PlanTier.FREE
    assert company.subscription_status == "canceled"
    db.close()