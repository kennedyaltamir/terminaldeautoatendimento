import pytest
from gerartxt import is_ignored, is_test_file

def test_is_test_file_detection():
    """Valida a lógica de detecção de arquivos de teste para economia de tokens."""
    assert is_test_file("tests/test_login.py") is True
    assert is_test_file("scripts/tests/test_api.py") is True
    assert is_test_file("frontend/e2e/flow.spec.ts") is True
    assert is_test_file("app/main.py") is False
    assert is_test_file("README.md") is False

def test_ignore_logic():
    """Valida se arquivos irrelevantes são ignorados."""
    # A função is_ignored agora exige uma lista de padrões gitignore como segundo argumento
    patterns = []
    
    assert is_ignored("node_modules/package.json", patterns) is True
    assert is_ignored(".git/config", patterns) is True
    assert is_ignored("app/main.pyc", patterns) is True
    assert is_ignored("app/main.py", patterns) is False
