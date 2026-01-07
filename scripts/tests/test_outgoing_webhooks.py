import pytest
import json
import hmac
import hashlib
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.webhook_dispatcher import WebhookDispatcher
from app.models import WebhookSubscription

@pytest.mark.asyncio
async def test_webhook_dispatch_integrity():
    """
    Valida o ciclo completo de um Webhook de Saída:
    1. Mock do Banco de Dados para retornar uma assinatura ativa.
    2. Execução do Dispatcher.
    3. Verificação da Assinatura HMAC-SHA256 enviada no Header.
    """
    # Dados de Teste
    company_id = "550e8400-e29b-41d4-a716-446655440000"
    target_url = "https://api.parceiro-enterprise.com/webhook"
    secret = "chave_mestra_de_teste_123"
    event = "order.created"
    payload = {
        "id": "order_abc_123",
        "total": 150.50,
        "customer": "Kennedy Oliveira"
    }

    # 1. Mock do Objeto de Assinatura no Banco
    mock_sub = MagicMock(spec=WebhookSubscription)
    mock_sub.target_url = target_url
    mock_sub.secret = secret
    mock_sub.events = [event]
    mock_sub.is_active = True

    # 2. Mock da Sessão do SQLAlchemy
    # Patch na SessionLocal usada dentro do dispatcher
    with patch("app.services.webhook_dispatcher.SessionLocal") as mock_session_factory:
        mock_db = MagicMock()
        mock_session_factory.return_value = mock_db
        
        # Configura a query para retornar nossa assinatura mockada
        mock_db.query.return_value.filter.return_value.all.return_value = [mock_sub]

        # 3. Mock do Cliente HTTP (httpx)
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            # Simula resposta 200 OK do servidor do cliente
            mock_post.return_value = MagicMock(status_code=200)

            # --- EXECUÇÃO ---
            await WebhookDispatcher.dispatch(event, payload, company_id)

            # --- VALIDAÇÕES ---
            
            # A. Verificou se o POST foi chamado
            assert mock_post.called, "O Dispatcher não tentou enviar o webhook."
            
            args, kwargs = mock_post.call_args
            
            # B. Validou a URL de destino
            assert args[0] == target_url
            
            # C. Validou o corpo da mensagem (JSON)
            sent_body_str = kwargs["content"]
            sent_json = json.loads(sent_body_str)
            assert sent_json["event"] == event
            assert sent_json["data"]["id"] == "order_abc_123"
            assert "timestamp" in sent_json

            # D. VALIDAÇÃO CRÍTICA: Assinatura HMAC
            # Recalculamos a assinatura aqui no teste para comparar com o que o Dispatcher enviou
            expected_signature = hmac.new(
                secret.encode(),
                sent_body_str.encode(),
                hashlib.sha256
            ).hexdigest()

            sent_signature = kwargs["headers"]["X-MesaFlow-Signature"]
            sent_event_header = kwargs["headers"]["X-MesaFlow-Event"]

            assert sent_event_header == event
            assert sent_signature == expected_signature, "A assinatura HMAC enviada é inválida ou corrompida."

            print(f"\n✅ Teste de Integridade de Webhook passou!")
            print(f"   URL: {target_url}")
            print(f"   Signature: {sent_signature}")

if __name__ == "__main__":
    # Permite rodar o script individualmente para debug rápido
    asyncio.run(test_webhook_dispatch_integrity())
