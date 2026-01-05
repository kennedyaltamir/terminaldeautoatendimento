from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company
from datetime import datetime, timedelta

client = TestClient(app)

def test_order_history_pagination():
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar 15 pedidos para testar paginação (Limit 10)
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    for i in range(15):
        order = Order(
            company_id=company.id,
            table_id=1,
            total_amount=10.00,
            status=OrderStatus.DELIVERED,
            payment_status=PaymentStatus.PAID,
            created_at=datetime.now()
        )
        db.add(order)
    db.commit()
    db.close()

    # 3. Testar Página 1
    res_p1 = client.get("/api/admin/hamburgueria-ze/history?page=1&limit=10", headers=headers)
    assert res_p1.status_code == 200
    data_p1 = res_p1.json()
    assert len(data_p1["data"]) == 10
    assert data_p1["total"] >= 15

    # 4. Testar Página 2
    res_p2 = client.get("/api/admin/hamburgueria-ze/history?page=2&limit=10", headers=headers)
    assert res_p2.status_code == 200
    data_p2 = res_p2.json()
    assert len(data_p2["data"]) >= 5 # Pelo menos os 5 restantes