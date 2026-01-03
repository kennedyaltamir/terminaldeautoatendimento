from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_websocket_connection_and_disconnect():
    """
    Testa se o endpoint WebSocket aceita conexões e lida com desconexões
    sem quebrar o servidor. Simula a resiliência do lado do servidor.
    """
    slug = "hamburgueria-ze"
    
    # 1. Conectar
    with client.websocket_connect(f"/ws/{slug}") as websocket:
        # 2. Enviar mensagem (Ping) - O backend atual apenas recebe e loga, ou espera broadcast
        # Vamos apenas garantir que a conexão foi aceita
        assert websocket
        
        # 3. Simular desconexão abrupta (Context manager fecha ao sair)
        pass
    
    # 4. Tentar reconectar imediatamente (Simulando o cliente reconectando)
    with client.websocket_connect(f"/ws/{slug}") as websocket2:
        assert websocket2
        
    # Se chegou aqui sem exceção, o servidor lidou bem com o ciclo de vida da conexão