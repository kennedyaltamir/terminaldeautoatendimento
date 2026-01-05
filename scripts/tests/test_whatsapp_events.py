import pytest
from unittest.mock import AsyncMock, patch
from app.services.whatsapp_service import WhatsAppService
from app.models import Company

@pytest.mark.asyncio
async def test_whatsapp_notification_triggers():
    """Valida se as strings de notificação são montadas corretamente."""
    company = Company(
        name="Teste Burguer",
        whatsapp_number="5511999999999",
        whatsapp_api_url="https://api.test",
        whatsapp_instance="i1",
        whatsapp_token="t1"
    )
    
    service = WhatsAppService()
    
    with patch.object(service, '_send_http_request', new_callable=AsyncMock) as mock_send:
        # 1. Testar Notificação de "Pronto"
        await service.notify_order_ready("João", "11999999999", "10", company.name, company)
        args = mock_send.call_args[0]
        assert "Mesa 10" in args[1]
        assert "Teste Burguer" in args[1]

        # 2. Testar Notificação de "Saída"
        await service.notify_delivery_dispatch("Maria", "11988888888", "Carlos", "id-123", "slug-loja", company)
        args = mock_send.call_args[0]
        assert "Carlos" in args[1]
        assert "slug-loja/menu?order=id-123" in args[1]
