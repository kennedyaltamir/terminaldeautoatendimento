from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from app.core.security import create_access_token
from decimal import Decimal
from datetime import datetime
import uuid

client = TestClient(app)

def test_franchise_dashboard_data_contract():
    """
    Valida se o endpoint de franquia retorna a estrutura de dados correta para o frontend.
    """
    # 1. Setup
    owner_email = f"franchise-contract-{uuid.uuid4().hex[:6]}@test.com"
    db = SessionLocal()
    
    # Loja A
    company_a = Company(name="Loja A", slug=f"loja-a-{uuid.uuid4().hex[:4]}", owner_email=owner_email)
    db.add(company_a)
    db.commit()
    
    # Pedido na Loja A
    db.add(Order(
        company_id=company_a.id, total_amount=100.00, 
        status=OrderStatus.DELIVERED, payment_status=PaymentStatus.PAID,
        created_at=datetime.now()
    ))
    db.commit()
    
    # Token
    token = create_access_token(data={"sub": owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Request
    res = client.get("/api/admin/franchise/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # 3. Validação de Contrato
    assert "total_revenue" in data
    assert "total_orders" in data
    assert "stores" in data
    assert isinstance(data["stores"], list)
    
    if len(data["stores"]) > 0:
        store = data["stores"][0]
        assert "id" in store
        assert "name" in store
        assert "slug" in store
        assert "revenue" in store
        assert "orders" in store
        
    print("✅ Contrato de dados de franquia validado!")
