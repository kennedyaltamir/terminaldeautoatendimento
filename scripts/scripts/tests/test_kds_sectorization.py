from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Category, Order, OrderItem, OrderStatus
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_kds_sectorization_data():
    """
    Valida se o backend fornece os dados de estação necessários para o refinamento do KDS.
    """
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(
        name=f"Sector Corp {unique_id}",
        slug=f"sector-{unique_id}",
        owner_email=f"sector-{unique_id}@test.com"
    )
    db.add(company)
    db.commit()
    
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    
    # Produto de Bar
    p_bar = Product(category_id=cat.id, name="Cerveja", price=10, station="bar")
    db.add(p_bar)
    db.commit()
    
    order = Order(company_id=company.id, total_amount=10, status=OrderStatus.PENDING)
    db.add(order)
    db.commit()
    
    item = OrderItem(order_id=order.id, product_id=p_bar.id, quantity=1, unit_price=10)
    db.add(item)
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    slug = company.slug
    db.close()

    # Request KDS
    res = client.get(f"/api/admin/{slug}/orders", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # Verifica se a estação 'bar' chegou no item do pedido
    assert data[0]["items"][0]["product"]["station"] == "bar"
