from fastapi.testclient import TestClient
from app.main import app
from app.models import PaymentMethod

client = TestClient(app)

def test_create_order_with_payment_method():
    """Valida se o pedido salva corretamente a forma de pagamento escolhida"""
    payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Cliente Pagador",
        "payment_method": "pix",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    response = client.post("/api/hamburgueria-ze/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["payment_method"] == "pix"
    assert data["payment_status"] == "pending"