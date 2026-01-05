from fastapi.testclient import TestClient
from app.main import app
from app.models import OrderStatus

client = TestClient(app)

def test_order_status_transition_for_kds():
    """Valida se o backend permite a transição de status que o KDS utiliza"""
    # 1. Login para obter token
    login_res = client.post(
        "/api/auth/token",
        data={"username": "adminmesaflow.com", "password": "123456"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Pegar um pedido pendente
    orders_res = client.get("/api/admin/hamburgueria-ze/orders", headers=headers)
    assert orders_res.status_code == 200
    orders = orders_res.json()
    
    if len(orders) > 0:
        order_id = orders[0]["id"]
        
        # 3. Atualizar para PREPARING
        patch_res = client.patch(
            f"/api/admin/orders/{order_id}",
            headers=headers,
            json={"status": "preparing"}
        )
        assert patch_res.status_code == 200
        
        # 4. Atualizar para READY
        patch_res = client.patch(
            f"/api/admin/orders/{order_id}",
            headers=headers,
            json={"status": "ready"}
        )
        assert patch_res.status_code == 200