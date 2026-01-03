import pytest
from unittest.mock import patch, AsyncMock
from app.services.fiscal.factory import FiscalFactory
from app.services.fiscal.providers.focus_nfe import FocusNFeProvider
from app.services.fiscal.providers.mock import MockFiscalProvider

def test_factory_returns_mock_by_default():
    """Se não configurar nada, deve retornar o Mock (Segurança)"""
    with patch.dict("os.environ", {}, clear=True):
        provider = FiscalFactory.get_provider()
        assert isinstance(provider, MockFiscalProvider)

def test_factory_returns_focus_when_configured():
    """Se configurar 'focus', deve retornar o provedor real"""
    with patch.dict("os.environ", {"FISCAL_PROVIDER": "focus"}):
        provider = FiscalFactory.get_provider()
        assert isinstance(provider, FocusNFeProvider)

@pytest.mark.asyncio
async def test_mock_provider_behavior():
    """Testa se o Mock retorna dados fake válidos"""
    provider = MockFiscalProvider()
    
    # Mock de objetos do banco
    order = AsyncMock()
    order.id = "123"
    company = AsyncMock()
    company.cnpj = "123"
    
    result = await provider.emit_nfc_e(order, company)
    
    assert result["status"] == "success"
    assert "sandbox" in result["nfe_url_pdf"]