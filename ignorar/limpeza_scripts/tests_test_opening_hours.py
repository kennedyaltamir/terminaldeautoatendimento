from fastapi.testclient import TestClient
from app.main import app
from datetime import time

client = TestClient(app)

def test_order_blocked_when_closed():
    """Valida se o pedido é bloqueado quando o restaurante está fora do horário"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Configurar horário para o passado (já fechado)
    # Ex: Abre 01:00, Fecha 01:01 (assumindo que o teste não roda nesse minuto)
    client.patch("/api/admin/company/me", headers=headers, json={
        "opens_at": "01:00:00",
        "closes_at": "01:01:00"
    })

    # 3. Tentar fazer pedido
    order_payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    response = client.post("/api/hamburgueria-ze/orders", json=order_payload)
    
    # Deve retornar 403 Forbidden
    assert response.status_code == 403
    assert "fechado" in response.json()["detail"]