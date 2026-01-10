# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 23:55:00
import httpx
import hmac
import hashlib
import json
import asyncio
from app.core.celery_app import celery_app
from app.core.logger import logger
from typing import Dict, Any

@celery_app.task(
    bind=True,
    max_retries=5,
    default_retry_delay=60, # 1 minuto inicial
    backoff_max=3600, # Máximo 1 hora
    autoretry_for=(httpx.RequestError, httpx.HTTPStatusError)
)
def dispatch_webhook_task(self, target_url: str, secret: str, event: str, payload: Dict[str, Any]):
    """
    Task Celery para envio de Webhook com retries persistentes.
    """
    logger.info(f"🔄 [Celery] Processando Webhook: {event} -> {target_url}")

    body_str = json.dumps(payload, default=str)
    
    # Assinatura HMAC
    signature = hmac.new(
        secret.encode(),
        body_str.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "MesaFlow-Webhook-Dispatcher/3.1",
        "X-MesaFlow-Event": event,
        "X-MesaFlow-Signature": signature
    }

    # Execução Síncrona (Celery Worker padrão é síncrono, usamos httpx.Client)
    # Se precisar de async, usaríamos asgiref.sync.async_to_sync, mas httpx.Client é suficiente aqui.
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(target_url, content=body_str, headers=headers)
            response.raise_for_status()
            
        logger.info(f"✅ [Celery] Webhook enviado com sucesso: {target_url} ({response.status_code})")
        return {"status": "success", "code": response.status_code}

    except Exception as e:
        logger.warning(f"⚠️ [Celery] Falha no envio ({self.request.retries}/5): {e}")
        # Retry exponencial (2^retries * delay)
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)
