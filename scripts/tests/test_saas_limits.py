from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, PlanTier, Product, Category, Order, OrderStatus, PaymentStatus
from datetime import datetime, timedelta
import uuid

client = TestClient(app)

def test_free_plan_product_limit():
    """
    Testa se o plano FREE bloqueia a criação de produtos após o limite (15).
    """
    # 1. Criar Empresa FREE
    unique_slug = f"limit-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Limit Test Corp",
        slug=unique_slug,
        owner_email=f"limit-{uuid.uuid4().hex[:6]}@test.com",
        plan_tier=PlanTier.FREE
    )
    db.add(company)
    db.commit()
    
    # Criar Categoria
    category = Category(company_id=company.id, name="Teste")
    db.add(category)
    db.commit()
    
    # CORREÇÃO: Salvar o ID antes de fechar a sessão
    category_id = category.id
    
    # Inserir 15 produtos (Limite)
    for i in range(15):
        p = Product(category_id=category.id, name=f"P{i}", price=10)
        db.add(p)
    db.commit()
    
    # Gerar Token
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Tentar criar o 16º produto (Deve falhar)
    payload = {
        "category_id": category_id, # Usando a variável local
        "name": "Produto Proibido",
        "price": 50.00
    }
    
    res = client.post("/api/admin/menu/products", headers=headers, json=payload)
    
    assert res.status_code == 402 # Payment Required
    assert "Limite" in res.json()["detail"]

def test_pro_plan_no_limit():
    """
    Testa se o plano PRO permite criar produtos ilimitados.
    """
    # 1. Criar Empresa PRO
    unique_slug = f"pro-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Pro Corp",
        slug=unique_slug,
        owner_email=f"pro-{uuid.uuid4().hex[:6]}@test.com",
        plan_tier=PlanTier.PRO
    )
    db.add(company)
    db.commit()
    
    category = Category(company_id=company.id, name="Teste")
    db.add(category)
    db.commit()
    
    # CORREÇÃO: Salvar o ID antes de fechar a sessão
    category_id = category.id
    
    # Inserir 15 produtos
    for i in range(15):
        p = Product(category_id=category.id, name=f"P{i}", price=10)
        db.add(p)
    db.commit()
    
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Tentar criar o 16º produto (Deve passar)
    payload = {
        "category_id": category_id, # Usando a variável local
        "name": "Produto Permitido",
        "price": 50.00
    }
    
    res = client.post("/api/admin/menu/products", headers=headers, json=payload)
    
    assert res.status_code == 201