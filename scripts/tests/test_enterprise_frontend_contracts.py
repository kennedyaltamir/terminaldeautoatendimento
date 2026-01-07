import pytest
from app.models import Company, Order, OrderStatus, PaymentStatus
from app.core.security import create_access_token
from decimal import Decimal
from datetime import datetime
import uuid

def test_marketing_and_franchise_contracts(client, db_session):
    """
    Valida se os endpoints de Marketing e Franquia retornam os dados
    no formato esperado pelo Frontend (React).
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    owner_email = f"ent-contract-{unique_id}@test.com"
    
    company = Company(
        name="Enterprise Corp", 
        slug=f"ent-{unique_id}", 
        owner_email=owner_email,
        loyalty_percentage=Decimal("5.00")
    )
    db_session.add(company)
    db_session.commit()
    
    # Criar um pedido pago para garantir que o dashboard tenha dados
    order = Order(
        company_id=company.id,
        total_amount=Decimal("100.00"),
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now()
    )
    db_session.add(order)
    db_session.commit()
    
    token = create_access_token(data={"sub": owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Teste Marketing (IA Trigger)
    res_mkt = client.post("/api/admin/marketing/recommendations/generate", headers=headers)
    assert res_mkt.status_code == 202
    
    # 3. Teste Franquia (Dashboard)
    res_fran = client.get("/api/admin/franchise/dashboard", headers=headers)
    assert res_fran.status_code == 200
    data = res_fran.json()
    
    # Validação de Contrato
    assert "total_revenue" in data
    assert "total_orders" in data
    assert isinstance(data["stores"], list)
    assert data["total_orders"] >= 1
