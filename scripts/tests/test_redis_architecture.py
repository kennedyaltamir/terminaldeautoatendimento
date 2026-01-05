import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.websockets import RedisConnectionManager
import json

@pytest.mark.asyncio
async def test_redis_broadcast_flow():
    """
    Testa se o broadcast publica no Redis e se o reader distribui localmente.
    Simula o fluxo completo sem precisar de um Redis real rodando no CI.
    """
    
    # 1. Mock do Redis
    mock_redis = AsyncMock()
    mock_pubsub = AsyncMock()
    
    # Configurar o mock do PubSub para simular recebimento de mensagem
    # O método listen retorna um async generator
    async def mock_listen():
        yield {
            "type": "message",
            "channel": "mesaflow:teste-slug",
            "data": json.dumps({"type": "new_order", "id": "123"})
        }
    
    mock_pubsub.listen = mock_listen
    mock_redis.pubsub.return_value = mock_pubsub

    # 2. Inicializar Manager com Mock
    manager = RedisConnectionManager()
    manager.redis_client = mock_redis
    manager.pubsub = mock_pubsub
    
    # 3. Simular Conexão de WebSocket Local
    mock_ws = AsyncMock()
    await manager.connect(mock_ws, "teste-slug")
    
    # Verificar se inscreveu no canal
    mock_pubsub.subscribe.assert_called_with("mesaflow:teste-slug")
    assert len(manager.active_connections["teste-slug"]) == 1

    # 4. Testar Broadcast (Publicação)
    payload = {"type": "new_order", "id": "123"}
    await manager.broadcast(payload, "teste-slug")
    
    # Verificar se publicou no Redis
    mock_redis.publish.assert_called_with(
        "mesaflow:teste-slug", 
        json.dumps(payload)
    )

    # 5. Testar Leitura e Distribuição (Simulando o loop do _redis_reader)
    # Como o _redis_reader é um loop infinito, vamos testar a lógica interna dele manualmente
    # simulando o que ele faria ao receber a mensagem do mock_listen definido acima.
    
    # Executa a lógica de distribuição local
    await manager._local_broadcast(payload, "teste-slug")
    
    # Verificar se o WebSocket local recebeu a mensagem
    mock_ws.send_json.assert_called_with(payload)
    
    print("✅ Fluxo Redis Pub/Sub validado com sucesso (Mock).")