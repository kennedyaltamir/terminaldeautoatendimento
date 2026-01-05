from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company, CustomerWallet
from decimal import Decimal
from app.core.security import create_access_token # <--- Import Adicionado
import uuid

client = TestClient(app)

def test_loyalty_cashback_trigger():
    """
    Testa se o cashback é creditado quando o pagamento é confirmado.
    """
    # 1. Setup
    unique_slug = f"loyalty-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Loyalty Corp",
        slug=unique_slug,
        owner_email=f"loyalty-{uuid.uuid4().hex[:6]}@test.com",
        loyalty_percentage=Decimal("10.00") # 10% Cashback
    )
    db.add(company)
    db.commit()
    
    # Pedido de R$ 100.00
    order = Order(
        company_id=company.id,
        customer_phone="11999998888",
        total_amount=Decimal("100.00"),
        status=OrderStatus.PENDING,
        payment_status=PaymentStatus.PENDING
    )
    db.add(order)
    db.commit()
    
    order_id = str(order.id)
    company_id = company.id
    
    # Gerar Token Admin
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Confirmar Pagamento (Simulando Admin ou Webhook)
    res = client.patch(f"/api/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    assert res.status_code == 200

    # 3. Verificar Carteira
    db = SessionLocal()
    wallet = db.query(CustomerWallet).filter(
        CustomerWallet.company_id == company_id,
        CustomerWallet.customer_phone == "11999998888"
    ).first()
    
    assert wallet is not None
    # 10% de 100 = 10
    assert wallet.balance == Decimal("10.00")
    
    # Verificar se o pedido registrou o ganho
    updated_order = db.query(Order).filter(Order.id == order_id).first()
    assert updated_order.cashback_earned == Decimal("10.00")
    
    db.close()

def test_metrics_sql_aggregation():
    """
    Testa se o novo endpoint de métricas SQL funciona.
    """
    # Reutiliza o setup anterior (já tem 1 pedido pago de R$ 100)
    db = SessionLocal()
    company = db.query(Company).filter(Company.name == "Loyalty Corp").first()
    if not company:
        return # Skip se rodar isolado sem o anterior
        
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    res = client.get("/api/admin/metrics", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    assert float(data["total_revenue"]) >= 100.00
    assert data["total_orders"] >= 1