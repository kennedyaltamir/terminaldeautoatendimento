import pytest
from unittest.mock import patch, AsyncMock
from app.services.whatsapp_service import WhatsAppService
from app.models import Company

@pytest.mark.asyncio
async def test_whatsapp_service_uses_company_config():
    """
    Testa se o serviço prioriza a configuração da empresa sobre a global.
    """
    service = WhatsAppService()
    
    # 1. Mock de Empresa com Config Própria
    company_custom = Company(
        whatsapp_api_url="https://api.custom.com",
        whatsapp_instance="custom_instance",
        whatsapp_token="custom_token"
    )
    
    # 2. Mock de Empresa sem Config (Deve usar Global/Fallback)
    company_default = Company(
        whatsapp_api_url=None
    )
    
    # Mock do HTTPX para não fazer chamada real
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        
        # Teste A: Config Customizada
        await service.notify_order_ready(
            "Cliente A", "5511999999999", "10", "Restaurante A", 
            company_settings=company_custom
        )
        
        # Verifica se usou a URL customizada
        args, _ = mock_post.call_args
        url_used = args[0]
        assert "api.custom.com" in url_used
        assert "custom_instance" in url_used

    # Teste B: Config Global (Simulando ENV)
    with patch.dict("os.environ", {
        "WHATSAPP_API_URL": "https://api.global.com",
        "WHATSAPP_INSTANCE": "global_inst",
        "WHATSAPP_API_TOKEN": "global_tok"
    }):
        # Recria serviço para ler ENV novo
        service_global = WhatsAppService()
        
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post_global:
            mock_post_global.return_value.status_code = 200
            
            await service_global.notify_order_ready(
                "Cliente B", "5511999999999", "11", "Restaurante B", 
                company_settings=company_default
            )
            
            args, _ = mock_post_global.call_args
            url_used = args[0]
            assert "api.global.com" in url_used
