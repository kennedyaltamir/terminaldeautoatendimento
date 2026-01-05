from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType
from decimal import Decimal
import uuid

client = TestClient(app)

def test_kiosk_order_flow():
    """
    Testa se o backend aceita pedidos 'Takeout' (padrão Kiosk) sem exigir mesa,
    e se processa múltiplos pedidos sequenciais corretamente.
    """
    # 1. Setup
    unique_slug = f"kiosk-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Kiosk Corp",
        slug=unique_slug,
        owner_email=f"kiosk-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Criar Produto
    from app.models import Category, Product
    cat = Category(company_id=company.id, name="Kiosk Menu")
    db.add(cat)
    db.commit()
    prod = Product(category_id=cat.id, name="Combo Kiosk", price=25.00)
    db.add(prod)
    db.commit()
    
    prod_id = prod.id
    company_id = company.id
    db.close()

    # 2. Pedido 1 (Cliente A no Totem)
    payload_1 = {
        "table_id": None,
        "qr_token": "staff-override", # Kiosk usa token de staff/sistema
        "order_type": "takeout",
        "customer_name": "Totem User 1",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    res_1 = client.post(f"/api/{unique_slug}/orders", json=payload_1)
    assert res_1.status_code == 201
    order_1 = res_1.json()
    assert order_1["customer_name"] == "Totem User 1"
    assert order_1["order_type"] == "takeout"

    # 3. Pedido 2 (Cliente B no Totem - Imediatamente após)
    payload_2 = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Totem User 2",
        "items": [{"product_id": prod_id, "quantity": 2}]
    }
    
    res_2 = client.post(f"/api/{unique_slug}/orders", json=payload_2)
    assert res_2.status_code == 201
    order_2 = res_2.json()
    assert order_2["customer_name"] == "Totem User 2"
    
    # 4. Verificar Banco
    db = SessionLocal()
    count = db.query(Order).filter(Order.company_id == company_id).count()
    assert count == 2
    db.close()
    
    print("✅ Fluxo de Kiosk (Takeout Sequencial) validado!")
