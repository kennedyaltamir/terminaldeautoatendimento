import httpx
import hmac
import hashlib
import json
import logging
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import WebhookSubscription, Company
from app.database import SessionLocal

logger = logging.getLogger("WebhookDispatcher")

class WebhookDispatcher:
    """
    Serviço responsável por notificar sistemas externos (Outgoing Webhooks).
    Implementa assinatura HMAC para segurança e retries para resiliência.
    """

    @staticmethod
    async def dispatch(event_name: str, payload: Dict[str, Any], company_id: str):
        """
        Dispara o evento para todas as URLs cadastradas pela empresa.
        Executado via BackgroundTasks para não bloquear a API.
        """
        db = SessionLocal()
        try:
            # 1. Buscar assinaturas ativas para este evento
            subscriptions = db.query(WebhookSubscription).filter(
                WebhookSubscription.company_id == company_id,
                WebhookSubscription.is_active == True
            ).all()

            if not subscriptions:
                return

            # Filtrar assinaturas que escutam este evento específico
            targets = [s for s in subscriptions if event_name in s.events]
            
            if not targets:
                return

            logger.info(f"🔔 [Webhook] Disparando '{event_name}' para {len(targets)} destinos (Company: {company_id})")

            # 2. Preparar o envelope do Webhook
            webhook_data = {
                "event": event_name,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": payload
            }
            body_str = json.dumps(webhook_data, default=str)

            # 3. Enviar para cada destino
            async with httpx.AsyncClient(timeout=10.0) as client:
                tasks = [
                    WebhookDispatcher._send_to_target(client, sub, body_str, event_name)
                    for sub in targets
                ]
                await asyncio.gather(*tasks)

        except Exception as e:
            logger.error(f"❌ [Webhook] Erro crítico no Dispatcher: {e}")
        finally:
            db.close()

    @staticmethod
    async def _send_to_target(client: httpx.AsyncClient, sub: WebhookSubscription, body: str, event: str):
        """Realiza o envio HTTP com assinatura e lógica de retry."""
        
        # Gerar Assinatura HMAC-SHA256
        signature = hmac.new(
            sub.secret.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MesaFlow-Webhook-Dispatcher/3.0",
            "X-MesaFlow-Event": event,
            "X-MesaFlow-Signature": signature
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await client.post(sub.target_url, content=body, headers=headers)
                
                if response.status_code >= 200 and response.status_code < 300:
                    logger.info(f"✅ [Webhook] Sucesso: {sub.target_url} (Status: {response.status_code})")
                    return
                
                logger.warning(f"⚠️ [Webhook] Falha (Tentativa {attempt+1}): {sub.target_url} (Status: {response.status_code})")
            
            except Exception as e:
                logger.warning(f"⚠️ [Webhook] Erro de conexão (Tentativa {attempt+1}): {sub.target_url} - {e}")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt) # Exponential backoff

        logger.error(f"❌ [Webhook] Desistindo após {max_retries} tentativas: {sub.target_url}")
