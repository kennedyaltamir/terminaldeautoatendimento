from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order_response_validation():
    """Valida se a resposta da criação de pedido agora inclui o objeto table corretamente"""
    payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Teste Validação",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    response = client.post("/api/hamburgueria-ze/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "table" in data
    assert data["table"]["table_number"] == 1
    assert "created_at" in data