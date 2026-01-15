from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus, FiscalStatus
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_fiscal_frontend_data_contract():
    """
    Valida se a API de histórico retorna os campos fiscais necessários para o Frontend.
    """
    # 1. Setup
    unique_slug = f"fiscal-front-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Fiscal Front Corp",
        slug=unique_slug,
        owner_email=f"ff-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Pedido com Nota Emitida
    order = Order(
        company_id=company.id,
        total_amount=Decimal("100.00"),
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        fiscal_status=FiscalStatus.EMITTED,
        nfe_url_pdf="https://nfe.url/pdf"
    )
    db.add(order)
    db.commit()
    
    order_id = str(order.id)
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Request Histórico
    res = client.get(f"/api/admin/{unique_slug}/history", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    target = next((o for o in data["data"] if o["id"] == order_id), None)
    assert target is not None
    
    # 3. Validação de Contrato
    assert "fiscal_status" in target
    assert target["fiscal_status"] == "emitted"
    assert "nfe_url_pdf" in target
    assert target["nfe_url_pdf"] == "https://nfe.url/pdf"
    
    print("✅ Contrato de dados fiscais para o frontend validado!")
