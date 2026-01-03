from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderType, OrderStatus
from decimal import Decimal
import uuid

client = TestClient(app)

def test_staff_create_delivery_order():
    """
    Testa se o staff consegue criar um pedido de Delivery sem mesa (table_id=None).
    """
    # 1. Setup
    unique_slug = f"delivery-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Delivery Corp",
        slug=unique_slug,
        owner_email=f"del-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Criar Produto
    from app.models import Category, Product
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    prod = Product(category_id=cat.id, name="Pizza", price=50.00)
    db.add(prod)
    db.commit()
    
    prod_id = prod.id
    db.close()

    # 2. Criar Pedido (Simulando App do Garçom)
    payload = {
        "table_id": None, # Sem mesa
        "qr_token": "staff-override", # Token mestre
        "order_type": "delivery",
        "customer_name": "Cliente Delivery",
        "customer_phone": "11999999999",
        "delivery_address": "Rua das Flores, 123",
        "payment_method": "cash",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    res = client.post(f"/api/{unique_slug}/orders", json=payload)
    assert res.status_code == 201
    data = res.json()
    
    assert data["order_type"] == "delivery"
    assert data["customer_name"] == "Cliente Delivery"
    assert data["delivery_address"] == "Rua das Flores, 123"
    assert data["status"] == "accepted" # Staff override já aceita automaticamente