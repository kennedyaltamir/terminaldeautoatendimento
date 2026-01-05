import os
import pytest
from gerartxt import check_secrets, is_ignored

def test_check_secrets():
    # Caso Seguro
    assert len(check_secrets("const a = 10;", "test.js")) == 0

    # Caso Perigoso (Simulação)
    content = "STRIPE_SECRET_KEY = 'sk_live_123456789012345678901234'"
    warnings = check_secrets(content, "config.py")
    assert len(warnings) > 0
    assert "POSSÍVEL SEGREDO" in warnings[0]

def test_ignore_logic_v6():
    # Teste de lógica de ignore atualizada
    patterns = []
    assert is_ignored("node_modules/react/index.js", patterns) is True
    assert is_ignored(".git/config", patterns) is True
    assert is_ignored("app/main.py", patterns) is False
