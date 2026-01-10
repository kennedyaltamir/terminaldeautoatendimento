# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-09 00:05:00
import logging
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import WebhookSubscription
from app.database import SessionLocal
# A lógica de envio real foi movida para app/tasks/webhooks.py para processamento assíncrono via Celery
from app.tasks.webhooks import dispatch_webhook_task

logger = logging.getLogger("WebhookDispatcher")

class WebhookDispatcher:
    """
    Serviço responsável por orquestrar o envio de Webhooks.
    Agora delega a execução real para o Celery (Fila Persistente).
    """

    @staticmethod
    async def dispatch(event_name: str, payload: dict, company_id: str):
        """
        Identifica assinantes e enfileira tasks no Celery.
        """
        db = SessionLocal()
        try:
            # 1. Buscar assinaturas ativas
            subscriptions = db.query(WebhookSubscription).filter(
                WebhookSubscription.company_id == company_id,
                WebhookSubscription.is_active == True
            ).all()

            if not subscriptions:
                return

            # Filtrar assinaturas
            targets = [s for s in subscriptions if event_name in s.events]

            if not targets:
                return

            logger.info(f"🔔 [Dispatcher] Enfileirando '{event_name}' para {len(targets)} destinos.")

            # 2. Preparar Envelope
            webhook_data = {
                "event": event_name,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": payload
            }

            # 3. Enfileirar no Celery (Fire and Forget)
            for sub in targets:
                # O método .delay() envia a tarefa para o Redis, não executa localmente.
                dispatch_webhook_task.delay(
                    target_url=sub.target_url,
                    secret=sub.secret,
                    event=event_name,
                    payload=webhook_data
                )

        except Exception as e:
            logger.error(f"❌ [Dispatcher] Erro ao enfileirar webhooks: {e}")
        finally:
            db.close()
