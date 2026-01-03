from fastapi.testclient import TestClient
from app.main import app
from app.models import PaymentStatus

client = TestClient(app)

def test_payment_confirmation_flow():
    """Valida se o admin consegue confirmar o pagamento de um pedido"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar um pedido
    order_payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Teste Pagamento",
        "payment_method": "pix",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    order_res = client.post("/api/hamburgueria-ze/orders", json=order_payload)
    order_id = order_res.json()["id"]

    # 3. Confirmar Pagamento
    pay_res = client.patch(f"/api/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    assert pay_res.status_code == 200
    
    # 4. Verificar se as métricas agora contam este pedido
    metrics_res = client.get("/api/admin/metrics", headers=headers)
    assert metrics_res.status_code == 200
    assert metrics_res.json()["total_orders"] >= 1