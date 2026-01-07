import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.fiscal.providers.focus_nfe import FocusNFeProvider
from app.models import Order, Company
from datetime import datetime

@pytest.mark.asyncio
async def test_focus_nfe_duplicity_handling_204():
    """
    Valida se o provedor FocusNFe trata corretamente o erro 422 de duplicidade,
    realizando o recovery da nota existente.
    """
    provider = FocusNFeProvider()
    
    # Setup Mocks
    company = Company(fiscal_token="fake_token")
    order = Order(id="order_123", customer_name="Test Client", created_at=datetime.now())
    order.items = []

    # Simulação da resposta de erro 422 (Duplicidade)
    mock_resp_422 = MagicMock()
    mock_resp_422.status_code = 422
    mock_resp_422.json.return_value = {
        "codigo": "requisicao_duplicada",
        "mensagem": "Ja existe um pedido com esta referencia"
    }

    # Simulação da resposta de recuperação (GET 200)
    mock_resp_200 = MagicMock()
    mock_resp_200.status_code = 200
    mock_resp_200.json.return_value = {
        "status": "autorizado",
        "ref": "order_123",
        "chave_nfe": "352301...KEY",
        "url_danfe": "https://focusnfe.com.br/pdf/123"
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_post.return_value = mock_resp_422
            mock_get.return_value = mock_resp_200

            result = await provider.emit_invoice(order, company)

            # Verificações
            assert result["status"] == "emitted"
            assert result["nfe_key"] == "352301...KEY"
            assert mock_get.called
            assert "nfce/order_123" in mock_get.call_args[0][0]

@pytest.mark.asyncio
async def test_fiscal_env_url_switch():
    """Garante que a URL muda conforme o FISCAL_ENV."""
    with patch.dict("os.environ", {"FISCAL_ENV": "sandbox"}):
        provider_sb = FocusNFeProvider()
        assert "homologacao" in provider_sb.base_url

    with patch.dict("os.environ", {"FISCAL_ENV": "production"}):
        provider_prod = FocusNFeProvider()
        assert "homologacao" not in provider_prod.base_url
