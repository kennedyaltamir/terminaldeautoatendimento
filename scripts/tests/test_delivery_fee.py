from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderType
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_delivery_fee_application():
    """
    Testa se a taxa de entrega fixa é aplicada corretamente ao pedido.
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(
        name=f"Fee Corp {unique_id}",
        slug=f"fee-{unique_id}",
        owner_email=f"fee-{unique_id}@test.com",
        fixed_delivery_fee=Decimal("5.00") # Taxa Fixa de R$ 5,00
    )
    db.add(company)
    db.commit()
    
    # Produto
    from app.models import Category, Product
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    prod = Product(category_id=cat.id, name="Item", price=10)
    db.add(prod)
    db.commit()
    
    prod_id = prod.id
    slug = company.slug
    db.close()

    # 2. Criar Pedido Delivery
    payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "delivery",
        "customer_name": "Fee Client",
        "customer_phone": "11999999999",
        "delivery_address": "Rua Fee",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    res = client.post(f"/api/{slug}/orders", json=payload)
    assert res.status_code == 201
    data = res.json()
    
    # 3. Validação
    # Subtotal: 10.00
    # Taxa: 5.00
    # Total: 15.00
    assert float(data["subtotal"]) == 10.00
    assert float(data["delivery_fee"]) == 5.00
    assert float(data["total_amount"]) == 15.00