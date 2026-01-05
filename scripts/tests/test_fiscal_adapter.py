import pytest
from unittest.mock import patch, AsyncMock
from app.services.fiscal.factory import get_fiscal_provider
from app.services.fiscal.providers.focus_nfe import FocusNFeProvider
from app.services.fiscal.providers.mock import MockProvider

def test_factory_returns_mock_by_default():
    """Se não configurar nada, deve retornar o Mock (Segurança)"""
    with patch.dict("os.environ", {}, clear=True):
        provider = get_fiscal_provider()
        assert isinstance(provider, MockProvider)

def test_factory_returns_focus_when_configured():
    """Se configurar 'focus', deve retornar o provedor real"""
    with patch.dict("os.environ", {"FISCAL_PROVIDER": "focus"}):
        provider = get_fiscal_provider()
        assert isinstance(provider, FocusNFeProvider)

@pytest.mark.asyncio
async def test_mock_provider_behavior():
    """Testa se o Mock retorna dados fake válidos"""
    provider = MockProvider()

    # Mock de objetos do banco
    order = AsyncMock()
    order.id = "123"
    company = AsyncMock()
    company.cnpj = "123"

    result = await provider.emit_invoice(order, company)

    assert result["status"] == "emitted"
    assert "sandbox" in result["nfe_url_pdf"]
