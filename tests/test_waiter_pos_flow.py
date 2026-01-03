from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession, Order, OrderStatus, PaymentStatus
import uuid

client = TestClient(app)

def test_waiter_close_table_flow():
    """
    Testa o fluxo de fechamento de mesa pelo garçom:
    1. Abre uma mesa.
    2. Lança um pedido.
    3. Fecha a mesa com pagamento em dinheiro.
    4. Verifica se a mesa ficou livre.
    """
    # 1. Login Admin
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup: Garantir Mesa 1 livre
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    table = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    db.query(TableSession).filter(TableSession.table_id == table.id).update({"is_active": False})
    db.commit()
    table_id = table.id
    db.close()

    # 3. Abrir Mesa
    open_res = client.post(f"/api/admin/tables/{table_id}/open", headers=headers, json={"customer_name": "Waiter Test"})
    assert open_res.status_code == 200

    # 4. Lançar Pedido (Staff Override)
    order_payload = {
        "table_id": table_id,
        "qr_token": "staff-override",
        "customer_name": "Waiter Test",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    order_res = client.post("/api/hamburgueria-ze/orders", json=order_payload)
    assert order_res.status_code == 201

    # 5. Fechar Mesa
    close_res = client.post(f"/api/admin/tables/{table_id}/close", headers=headers, json={"payment_method": "cash"})
    assert close_res.status_code == 200

    # 6. Verificar Status no Dashboard
    dash_res = client.get("/api/admin/tables/dashboard", headers=headers)
    tables = dash_res.json()
    table_1 = next(t for t in tables if t["table_number"] == 1)
    assert table_1["status"] == "free"