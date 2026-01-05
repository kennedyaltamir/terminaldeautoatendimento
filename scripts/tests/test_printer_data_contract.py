from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from decimal import Decimal
import uuid

client = TestClient(app)

def test_printer_data_contract_pix_code():
    """
    Valida se a API retorna o campo 'mp_qr_code' quando o pagamento é online.
    Isso é crítico para a função printer.qrCode() do frontend.
    """
    # 1. Setup
    unique_slug = f"print-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Print Corp",
        slug=unique_slug,
        owner_email=f"print-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Pedido com Pix (Simulado)
    order = Order(
        company_id=company.id,
        customer_name="Print Client",
        total_amount=Decimal("10.00"),
        status=OrderStatus.PENDING,
        payment_method="online",
        mp_qr_code="000201...TESTE_QR_CODE_PIX..."
    )
    db.add(order)
    db.commit()
    
    order_id = str(order.id)
    
    # Token
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Request (Usando endpoint de KDS que retorna lista)
    res = client.get(f"/api/admin/{unique_slug}/orders", headers=headers)
    assert res.status_code == 200
    orders = res.json()
    
    target = next((o for o in orders if o["id"] == order_id), None)
    assert target is not None
    
    # 3. Validação do Contrato
    assert "mp_qr_code" in target
    assert target["mp_qr_code"] == "000201...TESTE_QR_CODE_PIX..."
    
    print("✅ Contrato de dados para impressão validado!")