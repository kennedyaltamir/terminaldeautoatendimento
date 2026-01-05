import pytest
from gerartxt import is_test_file, deve_ignorar

def test_is_test_file_detection():
    """Valida a lógica de detecção de arquivos de teste para economia de tokens."""
    assert is_test_file("tests/test_login.py") is True
    assert is_test_file("scripts/tests/test_api.py") is True
    assert is_test_file("frontend/e2e/flow.spec.ts") is True
    assert is_test_file("app/main.py") is False
    assert is_test_file("README.md") is False

def test_ignore_logic():
    """Valida se arquivos irrelevantes são ignorados."""
    assert deve_ignorar("node_modules/package.json") is True
    assert deve_ignorar(".git/config") is True
    assert deve_ignorar("app/main.pyc") is True
    assert deve_ignorar("app/main.py") is False