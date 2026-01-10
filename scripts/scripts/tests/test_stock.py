from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Product, Company, Category
from decimal import Decimal
import uuid

client = TestClient(app)

def test_stock_decrement_and_block():
    # 1. Setup Isolado
    unique_slug = f"stock-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(name="Stock Corp", slug=unique_slug, owner_email=f"stock-{uuid.uuid4().hex[:6]}@test.com")
    db.add(company)
    db.commit()

    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()

    prod = Product(
        category_id=cat.id,
        name="Coca-Cola",
        price=Decimal("5.00"),
        track_stock=True,
        stock_quantity=5,
        is_available=True
    )
    db.add(prod)
    db.commit()
    prod_id = prod.id
    db.close()

    # 2. Comprar 3 Cocas
    order_payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "items": [{"product_id": prod_id, "quantity": 3}]
    }
    res_order = client.post(f"/api/{unique_slug}/orders", json=order_payload)
    assert res_order.status_code == 201
