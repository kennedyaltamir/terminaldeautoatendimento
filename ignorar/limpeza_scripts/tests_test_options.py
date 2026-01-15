from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Product, OptionGroup, Option, Company
import uuid

client = TestClient(app)

def test_order_with_options():
    """
    Testa o fluxo completo de um pedido com adicionais.
    """
    # 1. Setup Isolado
    unique_slug = f"opt-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    
    company = Company(
        name="Options Corp", 
        slug=unique_slug, 
        owner_email=f"opt-{unique_slug}@test.com",
        opens_at=None, # Aberto 24h
        closes_at=None
    )
    db.add(company)
    db.commit()

    from app.models import Category
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()

    product = Product(category_id=cat.id, name="Burger", price=20.00)
    db.add(product)
    db.commit()
    
    group = OptionGroup(product_id=product.id, name="Adicionais", min_selection=0, max_selection=5)
    db.add(group)
    db.commit()
    
    option = Option(group_id=group.id, name="Bacon Extra", price=3.50)
    db.add(option)
    db.commit()
    
    prod_id = product.id
    opt_id = option.id
    base_price = float(product.price)
    db.close()

    # 2. Criar Pedido com a opção
    payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Tester Options",
        "items": [
            {
                "product_id": prod_id,
                "quantity": 1,
                "selected_options": [opt_id]
            }
        ]
    }

    order_res = client.post(f"/api/{unique_slug}/orders", json=payload)
    
    if order_res.status_code != 201:
        print(f"Erro ao criar pedido: {order_res.json()}")

    assert order_res.status_code == 201

    # Validar Preço
    expected_total = base_price + 3.50
    assert float(order_res.json()["total_amount"]) == expected_total
