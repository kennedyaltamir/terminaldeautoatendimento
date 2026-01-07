import pytest
import os
from app.services.fiscal.factory import get_fiscal_provider
from unittest.mock import patch

def test_production_safeguard_blocks_without_confirmation():
    """
    Garante que o sistema lança RuntimeError se tentar ativar produção
    sem a flag de confirmação explícita.
    """
    with patch.dict(os.environ, {
        "FISCAL_ENV": "production",
        "FISCAL_PRODUCTION_CONFIRMED": "false",
        "FISCAL_PROVIDER": "focus"
    }):
        with pytest.raises(RuntimeError) as excinfo:
            get_fiscal_provider()
        assert "Ativação negada" in str(excinfo.value)

def test_production_safeguard_allows_with_confirmation():
    """
    Garante que o sistema permite a inicialização se ambas as flags estiverem corretas.
    """
    with patch.dict(os.environ, {
        "FISCAL_ENV": "production",
        "FISCAL_PRODUCTION_CONFIRMED": "true",
        "FISCAL_PROVIDER": "focus"
    }):
        provider = get_fiscal_provider()
        assert provider is not None
        # Não deve lançar exceção

def test_sandbox_does_not_require_confirmation():
    """
    Garante que o ambiente Sandbox continua funcionando normalmente sem a trava de produção.
    """
    with patch.dict(os.environ, {
        "FISCAL_ENV": "sandbox",
        "FISCAL_PROVIDER": "focus"
    }):
        provider = get_fiscal_provider()
        assert provider is not None
