# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-14 23:20:00
import os
import hmac
import hashlib
import logging
from fastapi import APIRouter, Request, HTTPException, Header, Depends
from app.database import SessionLocal
from app.services.ifood_service import IfoodService

router = APIRouter()
logger = logging.getLogger("IfoodWebhook")
ifood_service = IfoodService()

@router.post("/ifood")
async def ifood_webhook(
    request: Request,
    x_ifood_signature: str = Header(None)
):
    """
    Receiver de Webhooks do iFood com validação de integridade.
    """
    secret = os.getenv("IFOOD_WEBHOOK_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    body = await request.body()
    
    # Validação HMAC-SHA256
    expected_signature = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_ifood_signature or ""):
        logger.warning("🚨 Assinatura iFood inválida detectada!")
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    db = SessionLocal()
    try:
        # O iFood pode enviar uma lista de eventos
        events = payload if isinstance(payload, list) else [payload]
        for event in events:
            # Aqui buscaríamos a empresa pelo merchantId do payload
            # Para o MVP, processamos via polling service logic
            pass
        return {"status": "received"}
    finally:
        db.close()
