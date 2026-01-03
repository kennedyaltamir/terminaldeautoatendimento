from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Product

client = TestClient(app)

def test_stock_decrement_and_block():
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Verificar estoque inicial da Coca (5)
    # Precisamos do ID. Vamos pegar do menu.
    menu_res = client.get("/api/hamburgueria-ze/menu")
    data = menu_res.json()
    coca = next(p for cat in data["categories"] for p in cat["products"] if p["name"] == "Coca-Cola")
    assert coca["stock_quantity"] == 5

    # 3. Comprar 3 Cocas
    order_payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "items": [{"product_id": coca["id"], "quantity": 3}]
    }
    res_order = client.post("/api/hamburgueria-ze/orders", json=order_payload)
    assert res_order.status_code == 201

    # 4. Verificar se estoque caiu para 2
    menu_res_2 = client.get("/api/hamburgueria-ze/menu")
    coca_2 = next(p for cat in menu_res_2.json()["categories"] for p in cat["products"] if p["name"] == "Coca-Cola")
    assert coca_2["stock_quantity"] == 2

    # 5. Tentar comprar 3 Cocas (Só tem 2) -> Deve falhar
    res_fail = client.post("/api/hamburgueria-ze/orders", json=order_payload)
    assert res_fail.status_code == 400
    assert "insuficiente" in res_fail.json()["detail"]