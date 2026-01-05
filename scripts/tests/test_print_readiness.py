from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company, OrderItem, Product
from datetime import datetime
import uuid

client = TestClient(app)

def test_order_data_integrity_for_printing():
    """
    Valida se a API retorna todos os campos necessários para a impressão ESC/POS.
    Campos críticos: nome da empresa, data, itens, total, método de pagamento.
    """
    
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup de Dados
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Produto
    prod = db.query(Product).filter(Product.category.has(company_id=company.id)).first()
    
    # Pedido
    order = Order(
        company_id=company.id,
        table_id=1,
        total_amount=50.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        payment_method="cash",
        customer_name="Print Tester",
        created_at=datetime.now()
    )
    db.add(order)
    db.commit()
    
    item = OrderItem(order_id=order.id, product_id=prod.id, quantity=2, unit_price=25.00)
    db.add(item)
    db.commit()
    
    order_id = str(order.id)
    db.close()

    # 3. Buscar Pedido
    # A rota GET /api/admin/orders/{id} não existe (é PATCH e retorna 405).
    # Usamos a lista de recentes que é garantida para o admin e contém os dados completos.
    res = client.get(f"/api/admin/hamburgueria-ze/orders/recent-completed", headers=headers)
    assert res.status_code == 200
    orders = res.json()
    
    target_order = next((o for o in orders if o["id"] == order_id), None)
    assert target_order is not None, "Pedido não encontrado na lista de recentes"

    # 4. Validação de Campos Críticos para Impressão
    assert target_order["customer_name"] == "Print Tester"
    assert target_order["payment_method"] == "cash"
    assert float(target_order["total_amount"]) == 50.00
    assert len(target_order["items"]) > 0
    assert target_order["items"][0]["product"]["name"] is not None
    assert target_order["created_at"] is not None