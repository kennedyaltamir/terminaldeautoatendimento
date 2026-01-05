import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.websockets import RedisConnectionManager
import json

@pytest.mark.asyncio
async def test_redis_broadcast_flow():
    """
    Testa se o broadcast publica no Redis e se o reader distribui localmente.
    """
    # CORREÇÃO: O cliente Redis principal deve ser MagicMock (síncrono na criação)
    # para que .pubsub() não retorne uma corrotina.
    mock_redis_client = MagicMock()
    
    # Métodos assíncronos específicos são definidos como AsyncMock
    mock_redis_client.ping = AsyncMock(return_value=True)
    mock_redis_client.publish = AsyncMock()
    mock_redis_client.close = AsyncMock()
    
    # O pubsub é um objeto retornado sincronicamente
    mock_pubsub = MagicMock()
    mock_redis_client.pubsub.return_value = mock_pubsub
    
    # Métodos do pubsub são assíncronos
    mock_subscribe = AsyncMock()
    mock_pubsub.subscribe = mock_subscribe
    mock_pubsub.unsubscribe = AsyncMock()
    mock_pubsub.close = AsyncMock()

    # Simula o generator do listen
    async def mock_listen():
        yield {
            "type": "message",
            "channel": "mesaflow:teste-slug",
            "data": json.dumps({"type": "new_order", "id": "123"})
        }
    mock_pubsub.listen = mock_listen

    # Patch no local exato onde o redis é importado
    with patch("app.websockets.redis.from_url", return_value=mock_redis_client):
        manager = RedisConnectionManager()
        await manager.startup() 

        # Verifica se o modo Redis foi ativado
        assert manager.use_redis is True

        # Simula conexão WS
        mock_ws = AsyncMock()
        await manager.connect(mock_ws, "teste-slug")

        # Verifica subscrição
        assert mock_subscribe.called
        
        # Testar Broadcast (Publicação)
        payload = {"type": "new_order", "id": "123"}
        await manager.broadcast(payload, "teste-slug")

        # Verifica publicação
        assert mock_redis_client.publish.called
        args = mock_redis_client.publish.call_args[0]
        assert args[0] == "mesaflow:teste-slug"
        
        # Testar distribuição local
        await manager._local_broadcast(payload, "teste-slug")
        mock_ws.send_json.assert_called_with(payload)

        print("✅ Fluxo Redis Pub/Sub validado com sucesso (Mock).")
