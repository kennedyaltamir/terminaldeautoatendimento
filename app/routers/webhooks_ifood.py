
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 08:15:00
import os
import hmac
import hashlib
import json
import logging
from fastapi import APIRouter, Request, HTTPException, Header, Depends, BackgroundTasks
from app.database import SessionLocal
from app.services.ifood_service import IfoodService
from app.core.cache import CacheService

router = APIRouter()
logger = logging.getLogger("IfoodWebhook")
ifood_service = IfoodService()

# Security Configuration
IFOOD_WEBHOOK_SECRET = os.getenv("IFOOD_WEBHOOK_SECRET")
REPLAY_CACHE_TTL = 600  # 10 minutos para expiração de assinatura no cache

"""
SECURITY CONTRACT: IFOOD WEBHOOK (COMPLIANCE GRADE)
---------------------------------------------------
1. Auth Mechanism: HMAC-SHA256 Signature.
2. Headers: `x-ifood-signature` OR `X-IFood-Signature`.
3. Replay Protection: Redis-based Signature Deduplication (TTL 10m).
   - Prevents attacker from re-sending a captured valid payload.
4. Idempotency: Service Layer check on `external_order_id`.
5. Response: Always 200 OK (unless critical security failure) to prevent retry storms.
"""

async def verify_signature(request: Request):
    """
    Valida a assinatura HMAC e protege contra Replay Attacks.
    """
    # 1. Check Secret Presence
    if not IFOOD_WEBHOOK_SECRET:
        logger.error("CRITICAL: IFOOD_WEBHOOK_SECRET missing in environment.")
        raise HTTPException(status_code=500, detail="Security Configuration Error")

    # 2. Extract Signature
    signature = request.headers.get("x-ifood-signature") or request.headers.get("X-IFood-Signature")
    if not signature:
        logger.warning(f"Security: Missing signature from {request.client.host}")
        raise HTTPException(status_code=403, detail="Signature missing")

    # 3. Replay Protection (Redis Deduplication)
    # Verifica se esta assinatura já foi processada recentemente
    cache_key = f"webhook:ifood:sig:{signature}"
    if CacheService.get(cache_key):
        logger.warning(f"Security: Replay Attack detected. Signature {signature} already processed.")
        # Retorna 409 Conflict ou 200 OK (para silenciar o atacante/origem). 
        # 409 é semanticamente correto para conflito.
        raise HTTPException(status_code=409, detail="Duplicated Event (Replay Protection)")

    # 4. Compute HMAC
    body = await request.body()
    try:
        expected_signature = hmac.new(
            IFOOD_WEBHOOK_SECRET.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()
    except Exception as e:
        logger.error(f"HMAC Calculation Error: {e}")
        raise HTTPException(status_code=500, detail="Validation Error")

    # 5. Verify
    if not hmac.compare_digest(expected_signature, signature):
        logger.warning(f"Security: Invalid Signature. Expected {expected_signature}, got {signature}")
        raise HTTPException(status_code=403, detail="Invalid Signature")
        
    # 6. Lock Signature (Store in Redis)
    # Armazena a assinatura para impedir reuso nos próximos 10 minutos
    try:
        CacheService.set(cache_key, "processed", ttl=REPLAY_CACHE_TTL)
    except Exception as e:
        logger.error(f"Redis Cache Error: {e}")
        # Em caso de falha do Redis, prossegue mas loga o risco (Fail Open or Fail Close? Fail Open to not lose order)
        pass

async def process_event_background(payload: dict):
    db = SessionLocal()
    try:
        events = payload if isinstance(payload, list) else [payload]
        for event in events:
            await ifood_service.process_webhook_event(db, event)
        db.commit()
    except Exception as e:
        logger.error(f"Worker Error: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

@router.post("")
async def ifood_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    _auth: None = Depends(verify_signature)
):
    try:
        payload = await request.json()
        logger.info(f"Webhook Accepted. Payload size: {len(str(payload))} bytes")
        background_tasks.add_task(process_event_background, payload)
        return {"status": "received"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Endpoint Error: {e}")
        return {"status": "error_logged"}

