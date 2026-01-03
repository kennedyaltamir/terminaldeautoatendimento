from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, Company
import pytest

client = TestClient(app)

def test_whatsapp_notification_trigger_on_ready():
    """
    Testa se a função de atualização de status dispara a chamada para o serviço de WhatsApp
    quando o status muda para READY.
    """
    # 1. Login Admin
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup: Criar um pedido com telefone
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    order = Order(
        company_id=company.id,
        customer_name="Kennedy Test",
        customer_phone="11999999999",
        total_amount=50.00,
        status=OrderStatus.PREPARING
    )
    db.add(order)
    db.commit()
    order_id = str(order.id)
    db.close()

    # 3. Simular atualização para READY e verificar se o WhatsAppService foi chamado
    # Usamos patch no método notify_order_ready do WhatsAppService
    with patch("app.routers.admin.whatsapp_service.notify_order_ready", new_callable=AsyncMock) as mock_notify:
        mock_notify.return_value = True
        
        response = client.patch(
            f"/api/admin/orders/{order_id}",
            headers=headers,
            json={"status": "ready"}
        )
        
        assert response.status_code == 200
        # Verifica se o serviço de notificação foi acionado
        mock_notify.assert_called_once()
        
        # Verifica se os argumentos passados para a notificação estão corretos
        args, kwargs = mock_notify.call_args
        assert kwargs["customer_name"] == "Kennedy Test"
        assert kwargs["phone"] == "11999999999"