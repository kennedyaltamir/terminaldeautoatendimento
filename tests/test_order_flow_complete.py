from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_order_cycle_with_response_data():
    """Garante que o pedido criado retorna todos os dados necessários para o KDS e Impressão"""
    # 1. Criar Pedido
    payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Ciclo Completo",
        "payment_method": "pix",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    response = client.post("/api/hamburgueria-ze/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    
    # 2. Validar se os dados de impressão estão presentes
    assert "table" in data
    assert "items" in data
    assert len(data["items"]) > 0
    assert "product" in data["items"][0]
    assert "name" in data["items"][0]["product"]