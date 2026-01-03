from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_order_validation_logic():
    """Garante que o backend processa corretamente pedidos com e sem opções"""
    # 1. Pedido Simples (Sem opções)
    payload_simple = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Teste Simples",
        "items": [{"product_id": 3, "quantity": 1}] # Coca-Cola
    }
    res_simple = client.post("/api/hamburgueria-ze/orders", json=payload_simple)
    assert res_simple.status_code == 201
    assert float(res_simple.json()["total_amount"]) == 6.00

    # 2. Pedido com Opções (X-Bacon + Bacon Extra)
    # X-Bacon (28.90) + Bacon Extra (3.50) = 32.40
    payload_options = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Teste Opções",
        "items": [{
            "product_id": 1, 
            "quantity": 1,
            "selected_options": [4] # ID do Bacon Extra no seed
        }]
    }
    res_options = client.post("/api/hamburgueria-ze/orders", json=payload_options)
    assert res_options.status_code == 201
    assert float(res_options.json()["total_amount"]) == 32.40