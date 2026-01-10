from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Order, OrderItem, OrderStatus, PaymentStatus, Category
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_kds_station_data_integrity():
    """
    Testa se a API retorna os dados de 'station' corretamente para que o frontend
    possa realizar a filtragem por praça (Bar/Cozinha).
    """
    # 1. Setup
    unique_slug = f"station-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Station Corp",
        slug=unique_slug,
        owner_email=f"station-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    
    # Produto de Cozinha
    burger = Product(
        category_id=cat.id,
        name="Burger Station",
        price=10.0,
        station="kitchen"
    )
    
    # Produto de Bar
    drink = Product(
        category_id=cat.id,
        name="Drink Station",
        price=10.0,
        station="bar"
    )
    
    db.add_all([burger, drink])
    db.commit()
    
    # Pedido Misto
    order = Order(
        company_id=company.id,
        customer_name="Mixed Order",
        total_amount=20.0,
        status=OrderStatus.PENDING,
        payment_status=PaymentStatus.PAID
    )
    db.add(order)
    db.commit()
    
    item1 = OrderItem(order_id=order.id, product_id=burger.id, quantity=1, unit_price=10.0)
    item2 = OrderItem(order_id=order.id, product_id=drink.id, quantity=1, unit_price=10.0)
    db.add_all([item1, item2])
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Request KDS
    res = client.get(f"/api/admin/{unique_slug}/orders", headers=headers)
    assert res.status_code == 200
    orders = res.json()
    
    assert len(orders) > 0
    target_order = orders[0]
    
    # 3. Validação de Dados para o Frontend
    # O frontend precisa que cada item tenha product.station
    items = target_order["items"]
    assert len(items) == 2
    
    # Verificar se os stations vieram corretos
    stations = [item["product"]["station"] for item in items]
    assert "kitchen" in stations
    assert "bar" in stations
    
    print("✅ Dados de estação validados com sucesso!")