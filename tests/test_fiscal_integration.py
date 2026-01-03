from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus, FiscalStatus
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_fiscal_emission_flow():
    """
    Testa o fluxo de emissão de nota fiscal:
    1. Configura empresa com tokens fiscais.
    2. Cria pedido pago.
    3. Chama endpoint de emissão.
    4. Verifica se a URL da nota foi salva.
    """
    # 1. Setup
    unique_slug = f"fiscal-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Fiscal Corp",
        slug=unique_slug,
        owner_email=f"fiscal-{uuid.uuid4().hex[:6]}@test.com",
        fiscal_token="TOKEN_TESTE_123",
        csc_token="CSC_TESTE_456",
        cnpj="12345678000199"
    )
    db.add(company)
    db.commit()
    
    order = Order(
        company_id=company.id,
        total_amount=Decimal("50.00"),
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        customer_name="Fiscal Client"
    )
    db.add(order)
    db.commit()
    
    order_id = str(order.id)
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Emitir Nota
    res = client.post(f"/api/admin/fiscal/orders/{order_id}/emit", headers=headers)
    
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "nfe_url" in data
    assert "pdf" in data["nfe_url"]

    # 3. Verificar Persistência
    db = SessionLocal()
    updated_order = db.query(Order).filter(Order.id == order_id).first()
    assert updated_order.fiscal_status == FiscalStatus.EMITTED
    assert updated_order.nfe_key is not None
    db.close()