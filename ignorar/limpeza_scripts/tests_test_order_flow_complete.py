from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Category
import uuid

client = TestClient(app)

def test_full_order_cycle_with_response_data():
    """Garante que o pedido criado retorna todos os dados necessários"""
    # 1. Setup Isolado
    unique_slug = f"cycle-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Cycle Corp", 
        slug=unique_slug, 
        owner_email=f"cycle-{unique_slug}@test.com",
        opens_at=None,
        closes_at=None
    )
    db.add(company)
    db.commit()
    
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()

    prod = Product(category_id=cat.id, name="Item Cycle", price=10.00)
    db.add(prod)
    db.commit()
    
    prod_id = prod.id
    db.close()

    # 2. Criar Pedido
    payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Ciclo Completo",
        "payment_method": "pix",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    response = client.post(f"/api/{unique_slug}/orders", json=payload)
    
    if response.status_code != 201:
        print(f"Erro: {response.json()}")

    assert response.status_code == 201
    data = response.json()

    # 3. Validar
    assert "items" in data
    assert len(data["items"]) > 0
