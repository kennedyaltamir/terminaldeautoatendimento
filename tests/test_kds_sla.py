from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company
from datetime import datetime, timedelta

client = TestClient(app)

def test_kds_order_sorting_by_time():
    """
    Verifica se a API retorna os pedidos ordenados por data de criação (FIFO).
    Isso é crucial para o SLA funcionar visualmente no frontend.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar pedidos com timestamps diferentes
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Pedido Antigo (Deve aparecer primeiro)
    order_old = Order(
        company_id=company.id,
        table_id=1,
        total_amount=10.00,
        status=OrderStatus.PENDING,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now() - timedelta(minutes=30) # Atrasado (Vermelho)
    )
    
    # Pedido Novo (Deve aparecer depois)
    order_new = Order(
        company_id=company.id,
        table_id=1,
        total_amount=20.00,
        status=OrderStatus.PENDING,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now() # Novo (Verde)
    )
    
    db.add_all([order_old, order_new])
    db.commit()
    
    # IDs para verificação
    old_id = str(order_old.id)
    new_id = str(order_new.id)
    
    db.close()

    # 3. Buscar KDS
    res = client.get("/api/admin/hamburgueria-ze/orders", headers=headers)
    assert res.status_code == 200
    orders = res.json()
    
    # Filtrar apenas os nossos pedidos de teste
    test_orders = [o for o in orders if o["id"] in [old_id, new_id]]
    
    # O pedido antigo deve vir antes do novo na lista (FIFO)
    assert test_orders[0]["id"] == old_id
    assert test_orders[1]["id"] == new_id