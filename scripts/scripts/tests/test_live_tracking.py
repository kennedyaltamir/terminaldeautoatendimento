from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole
from app.core.security import create_access_token
from unittest.mock import patch, AsyncMock
import uuid

client = TestClient(app)

def test_tracking_link_generation():
    """
    Testa se o link de rastreamento é gerado corretamente na mensagem de WhatsApp.
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()

    company = Company(name=f"Track Corp {unique_id}", slug=f"track-{unique_id}", owner_email=f"track-{unique_id}@test.com")
    db.add(company)
    db.commit()

    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.READY,
        customer_name="Track Client",
        customer_phone="11999999999",
        total_amount=50.00
    )
    db.add(order)
    db.commit()

    order_id = str(order.id)
    slug = company.slug

    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}

    db.close()

    # 2. Mock do WhatsApp Service (Método correto: notify_delivery_dispatch)
    with patch("app.services.whatsapp_service.WhatsAppService.notify_delivery_dispatch", new_callable=AsyncMock) as mock_notify:
        mock_notify.return_value = True

        # 3. Despachar Pedido
        res = client.patch(f"/api/admin/delivery/orders/{order_id}/dispatch", headers=headers, json={})
        assert res.status_code == 200

        # 4. Verificar Chamada
        mock_notify.assert_called_once()
        
        # Verificar argumentos nomeados
        kwargs = mock_notify.call_args.kwargs
        assert kwargs['customer_name'] == "Track Client"
        assert kwargs['phone'] == "11999999999"
        assert kwargs['order_id'] == order_id
        assert kwargs['slug'] == slug
