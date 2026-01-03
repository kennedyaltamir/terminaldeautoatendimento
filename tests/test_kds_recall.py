from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company
from datetime import datetime

client = TestClient(app)

def test_kds_recall_flow():
    """
    Testa o fluxo de Recall:
    1. Criar pedido finalizado (DELIVERED).
    2. Buscar na lista de 'recent-completed'.
    3. Restaurar para 'PREPARING'.
    4. Verificar se voltou para a lista principal.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar pedido finalizado
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    order = Order(
        company_id=company.id,
        table_id=1,
        total_amount=50.00,
        status=OrderStatus.DELIVERED, # Já finalizado
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now(),
        finished_at=datetime.now()
    )
    db.add(order)
    db.commit()
    order_id = str(order.id)
    db.close()

    # 3. Buscar na lista de Recall
    recall_res = client.get("/api/admin/hamburgueria-ze/orders/recent-completed", headers=headers)
    assert recall_res.status_code == 200
    recent_orders = recall_res.json()
    assert any(o["id"] == order_id for o in recent_orders)

    # 4. Restaurar (Recall)
    restore_res = client.patch(f"/api/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
    assert restore_res.status_code == 200

    # 5. Verificar se voltou para a lista principal (KDS Ativo)
    kds_res = client.get("/api/admin/hamburgueria-ze/orders", headers=headers)
    active_orders = kds_res.json()
    assert any(o["id"] == order_id for o in active_orders)
    
    # Verificar status
    restored_order = next(o for o in active_orders if o["id"] == order_id)
    assert restored_order["status"] == "preparing"