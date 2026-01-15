from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Category, Order, OrderItem, OrderStatus
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def setup_kds_env():
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(
        name=f"KDS {unique_id}",
        slug=f"kds-{unique_id}",
        owner_email=f"kds-{unique_id}@test.com"
    )
    db.add(company)
    db.commit()
    
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    
    p_kitchen = Product(category_id=cat.id, name="Burger", price=20, station="kitchen")
    p_bar = Product(category_id=cat.id, name="Gin", price=25, station="bar")
    db.add_all([p_kitchen, p_bar])
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    
    return db, company, p_kitchen, p_bar, token

def test_kds_01_mixed_order_filtering():
    """KDS-01: Pedido Misto aparece com itens filtrados"""
    db, company, p_kitchen, p_bar, token = setup_kds_env()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Criar Pedido Misto
    order = Order(company_id=company.id, customer_name="Misto", total_amount=45, status=OrderStatus.PENDING)
    db.add(order)
    db.commit()
    
    i1 = OrderItem(order_id=order.id, product_id=p_kitchen.id, quantity=1, unit_price=20)
    i2 = OrderItem(order_id=order.id, product_id=p_bar.id, quantity=1, unit_price=25)
    db.add_all([i1, i2])
    db.commit()
    
    # Extrair slug antes de fechar
    slug = company.slug
    db.close()
    
    # O Backend retorna o pedido completo. O filtro é no Frontend, 
    # mas o backend DEVE retornar a info 'station' no produto.
    
    res = client.get(f"/api/admin/{slug}/orders", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    order_data = data[0]
    items = order_data["items"]
    
    # Validar se a info de estação está presente
    stations = [item["product"]["station"] for item in items]
    assert "kitchen" in stations
    assert "bar" in stations

def test_kds_03_recall():
    """KDS-03: Recall (Restaurar pedido finalizado)"""
    db, company, _, _, token = setup_kds_env()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Pedido Finalizado
    order = Order(company_id=company.id, customer_name="Recall Me", total_amount=10, status=OrderStatus.DELIVERED)
    db.add(order)
    db.commit()
    
    # Extrair dados antes de fechar
    order_id = str(order.id)
    slug = company.slug
    db.close()
    
    # Restaurar
    res = client.patch(f"/api/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
    assert res.status_code == 200
    
    # Verificar se voltou para a lista ativa
    res_list = client.get(f"/api/admin/{slug}/orders", headers=headers)
    active_ids = [o["id"] for o in res_list.json()]
    assert order_id in active_ids

def test_kds_04_quick_stock_86():
    """KDS-04: Bloqueio Rápido de Estoque (86)"""
    db, company, p_kitchen, _, token = setup_kds_env()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Extrair dados antes de fechar
    prod_id = p_kitchen.id
    slug = company.slug
    
    # Bloquear Burger
    res = client.patch(
        f"/api/admin/menu/products/{prod_id}", 
        headers=headers, 
        json={"is_available": False}
    )
    assert res.status_code == 200
    
    db.close()
    
    # Tentar pedir (Deve falhar)
    payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout", # <--- CORREÇÃO: Tipo Takeout para não exigir mesa
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    res_order = client.post(f"/api/{slug}/orders", json=payload)
    assert res_order.status_code == 400
    assert "indisponível" in res_order.json()["detail"]