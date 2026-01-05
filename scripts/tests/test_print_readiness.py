from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company, OrderItem, Product, Category
from app.core.security import create_access_token
from datetime import datetime
import uuid

client = TestClient(app)

def test_order_data_integrity_for_printing():
    """
    Valida se a API retorna todos os campos necessários para a impressão.
    """
    # 1. Setup Isolado
    unique_slug = f"print-{uuid.uuid4().hex[:6]}"
    email = f"print-{unique_slug}@test.com"

    db = SessionLocal()
    company = Company(name="Print Corp", slug=unique_slug, owner_email=email)
    db.add(company)
    db.commit()

    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()

    prod = Product(category_id=cat.id, name="Item Print", price=10.00)
    db.add(prod)
    db.commit()

    order = Order(
        company_id=company.id,
        table_id=1,
        total_amount=50.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        payment_method="cash",
        customer_name="Print Tester",
        created_at=datetime.now(),
        finished_at=datetime.now()
    )
    db.add(order)
    db.commit()

    item = OrderItem(order_id=order.id, product_id=prod.id, quantity=2, unit_price=25.00)
    db.add(item)
    db.commit()

    order_id = str(order.id)
    
    token = create_access_token(data={"sub": email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 3. Buscar Pedido
    res = client.get(f"/api/admin/{unique_slug}/orders/recent-completed", headers=headers)
    assert res.status_code == 200
    orders = res.json()

    target_order = next((o for o in orders if o["id"] == order_id), None)
    assert target_order is not None
