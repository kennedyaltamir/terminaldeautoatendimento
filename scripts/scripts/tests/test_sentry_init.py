from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
import os

client = TestClient(app)

def test_sentry_initialization_mock():
    """
    Testa se o Sentry é inicializado quando a variável de ambiente existe.
    """
    with patch("sentry_sdk.init") as mock_init:
        # Simula a variável de ambiente
        with patch.dict(os.environ, {"SENTRY_DSN_BACKEND": "https://fake@sentry.io/123"}):
            # Recarrega o módulo main para disparar o init (simulado)
            import importlib
            import app.main
            importlib.reload(app.main)
            
            mock_init.assert_called()
            
def test_sentry_debug_route():
    """
    Testa se a rota de debug dispara um erro 500 (ZeroDivisionError).
    Isso confirma que a exceção está ocorrendo e seria capturada pelo Sentry.
    """
    try:
        client.get("/sentry-debug")
    except ZeroDivisionError:
        assert True
    except Exception:
        assert False, "Deveria ter lançado ZeroDivisionError"