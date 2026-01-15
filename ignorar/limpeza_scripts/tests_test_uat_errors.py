from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Category
from decimal import Decimal
import uuid

client = TestClient(app)

def test_err_02_stock_race_condition():
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    company = Company(name=f"Err {unique_id}", slug=f"err-{unique_id}", owner_email=f"err-{unique_id}@test.com")
    db.add(company)
    db.commit()

    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()

    prod = Product(category_id=cat.id, name="Last Item", price=10, track_stock=True, stock_quantity=1)
    db.add(prod)
    db.commit()
    prod_id = prod.id
    slug = company.slug
    db.close()

    # Pedido 1 (Sucesso)
    payload = {
        "table_id": None, "qr_token": "staff-override", "order_type": "takeout",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    client.post(f"/api/{slug}/orders", json=payload)

    # Pedido 2 (Falha)
    res2 = client.post(f"/api/{slug}/orders", json=payload)
    assert res2.status_code == 400
    # Mensagem flexível
    assert "estoque" in res2.json()["detail"].lower() or "indisponível" in res2.json()["detail"].lower()
