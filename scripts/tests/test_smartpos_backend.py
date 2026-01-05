from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, PaymentMethod
from decimal import Decimal
import uuid

client = TestClient(app)

def test_backend_accepts_smartpos_order():
    """
    Testa se o backend aceita um pedido com as características de um SmartPOS:
    - Tipo: Takeout (Balcão/Kiosk)
    - Pagamento: Card (Cartão)
    - Sem Mesa (table_id=None)
    """
    # 1. Setup
    unique_slug = f"smartpos-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="SmartPOS Corp",
        slug=unique_slug,
        owner_email=f"smart-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Criar Produto
    from app.models import Category, Product
    cat = Category(company_id=company.id, name="Kiosk Menu")
    db.add(cat)
    db.commit()
    prod = Product(category_id=cat.id, name="Combo Smart", price=10.00)
    db.add(prod)
    db.commit()
    
    prod_id = prod.id
    company_id = company.id
    db.close()

    # 2. Criar Pedido (Simulando Kiosk)
    payload = {
        "table_id": None,
        "qr_token": "staff-override", # Kiosk usa token de sistema
        "order_type": "takeout",
        "customer_name": "SmartPOS User",
        "payment_method": "card", # Pagamento via Maquininha
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    res = client.post(f"/api/{unique_slug}/orders", json=payload)
    assert res.status_code == 201
    
    data = res.json()
    assert data["order_type"] == "takeout"
    assert data["payment_method"] == "card"
    assert data["status"] == "accepted" # Staff override aceita direto
    
    # 3. Verificar Banco
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == data["id"]).first()
    assert order is not None
    assert order.payment_method == PaymentMethod.CARD
    db.close()
    
    print("✅ Backend validado para fluxo SmartPOS!")