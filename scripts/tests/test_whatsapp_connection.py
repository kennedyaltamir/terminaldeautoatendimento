import pytest
from unittest.mock import AsyncMock, patch
from app.services.whatsapp_service import WhatsAppService
from app.models import Company

@pytest.mark.asyncio
async def test_whatsapp_send_test_message_success():
    # Mock da empresa com configurações válidas
    company = Company(
        whatsapp_number="5511999999999",
        whatsapp_api_url="https://api.fake.com",
        whatsapp_instance="instance_1",
        whatsapp_token="token_123"
    )

    service = WhatsAppService()

    # Mock do httpx.AsyncClient
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        
        result = await service.send_test_message(company)
        
        assert result is True
        mock_post.assert_called_once()
        
        # Verifica se a URL foi montada corretamente
        args, kwargs = mock_post.call_args
        assert "https://api.fake.com/message/sendText/instance_1" in args[0]
        assert kwargs["json"]["number"] == "5511999999999"

@pytest.mark.asyncio
async def test_whatsapp_send_test_message_no_number():
    company = Company(whatsapp_number=None)
    service = WhatsAppService()
    
    result = await service.send_test_message(company)
    assert result is False

@pytest.mark.asyncio
async def test_whatsapp_send_test_message_api_fail():
    company = Company(
        whatsapp_number="5511999999999",
        whatsapp_api_url="https://api.fake.com",
        whatsapp_instance="instance_1",
        whatsapp_token="token_123"
    )
    
    service = WhatsAppService()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 401 # Unauthorized
        
        result = await service.send_test_message(company)
        assert result is False
