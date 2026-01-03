from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, Company, Table
from unittest.mock import patch, AsyncMock
import uuid

client = TestClient(app)

def test_websocket_notification_payload_structure():
    """
    Testa se o payload enviado pelo WebSocket contém os campos necessários
    para o frontend disparar a vibração e o som.
    """
    # 1. Setup
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    table = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    
    order = Order(
        company_id=company.id,
        table_id=table.id,
        customer_name="Vibration Test",
        total_amount=10.00,
        status=OrderStatus.PREPARING
    )
    db.add(order)
    db.commit()
    order_id = str(order.id)
    db.close()

    # 2. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Mock do WebSocket Manager para interceptar a mensagem
    with patch("app.websockets.manager.broadcast", new_callable=AsyncMock) as mock_broadcast:
        # Atualizar status para READY
        client.patch(f"/api/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
        
        # 4. Verificar Payload
        mock_broadcast.assert_called()
        args, _ = mock_broadcast.call_args
        message = args[0]
        
        # Campos obrigatórios para o NotificationManager.tsx
        assert message["type"] == "order_update"
        assert message["status"] == "ready"
        assert "table" in message # Usado para o título do Toast
        assert str(message["table"]) == "1"