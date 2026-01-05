import pytest
import os
from gerartxt import is_ignored, check_secrets, minify_content, is_test_file, get_dependencies

def test_ignore_logic_v3():
    # Pastas (Com barras normais, o script deve normalizar)
    assert is_ignored("node_modules/react/index.js", []) is True
    assert is_ignored(".git/config", []) is True
    
    # Extensões
    assert is_ignored("image.png", []) is True
    assert is_ignored("app.exe", []) is True
    
    # Arquivos Válidos
    assert is_ignored("app/main.py", []) is False
    assert is_ignored("frontend/src/index.ts", []) is False

def test_secret_detection():
    # Caso Seguro
    assert len(check_secrets("const a = 10;", "test.js")) == 0
    
    # Caso Perigoso
    content = "STRIPE_SECRET_KEY = 'sk_live_123456789012345678901234'"
    warnings = check_secrets(content, "config.py")
    assert len(warnings) > 0
    assert "POSSÍVEL SEGREDO" in warnings[0]

def test_minification():
    original = "def func():\n\n\n    return True"
    expected = "def func():\n\n    return True"
    assert minify_content(original) == expected

def test_test_file_detection():
    assert is_test_file("tests/test_api.py") is True
    assert is_test_file("frontend/e2e/flow.spec.ts") is True
    assert is_test_file("app/services/payment.py") is False

def test_dependency_extraction():
    # Mock simples para garantir que a função roda sem erro
    deps = get_dependencies()
    assert isinstance(deps, str)
