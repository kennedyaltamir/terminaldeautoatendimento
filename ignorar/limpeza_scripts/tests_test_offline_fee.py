from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession, Order, OrderStatus, PaymentStatus
from decimal import Decimal
import uuid

client = TestClient(app)

def test_offline_fee_accumulation():
    """
    Testa se a comissão de vendas em dinheiro é acumulada corretamente no saldo devedor da empresa.
    """
    # 1. Setup
    unique_slug = f"fee-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Fee Corp",
        slug=unique_slug,
        owner_email=f"fee-{uuid.uuid4().hex[:6]}@test.com",
        marketplace_fee_percentage=Decimal("2.50"), # 2.5% de taxa
        pending_commission_balance=Decimal("0.00")
    )
    db.add(company)
    db.commit()
    db.refresh(company) # Garante ID
    
    # Criar Mesa e Sessão
    table = Table(company_id=company.id, table_number=1, qr_token="token")
    db.add(table)
    db.commit()
    
    session = TableSession(
        company_id=company.id, table_id=table.id, customer_name="Fee Payer",
        session_token=str(uuid.uuid4()), access_pin="0000", is_active=True
    )
    db.add(session)
    db.commit()
    
    # Criar Pedido de R$ 100.00
    order = Order(
        company_id=company.id, session_id=session.id, table_id=table.id,
        total_amount=Decimal("100.00"), status=OrderStatus.PENDING
    )
    db.add(order)
    db.commit()
    
    company_id = company.id
    table_id = table.id
    
    # Token Admin
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Fechar Mesa com Dinheiro
    res = client.post(
        f"/api/admin/tables/{table_id}/close",
        headers=headers,
        json={"payment_method": "cash"}
    )
    assert res.status_code == 200

    # 3. Verificar Saldo Devedor
    db = SessionLocal()
    updated_company = db.query(Company).filter(Company.id == company_id).first()
    
    # 2.5% de 100 = 2.50
    assert updated_company.pending_commission_balance == Decimal("2.50")
    
    db.close()