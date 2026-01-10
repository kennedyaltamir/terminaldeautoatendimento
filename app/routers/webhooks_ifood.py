# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 09:58:00
import os
import hmac
import hashlib
import json
from fastapi import APIRouter, Request, HTTPException, Header, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ifood_service import IfoodService
from app.models import Company

router = APIRouter()
ifood_service = IfoodService()

# Segredo configurado no portal do desenvolvedor do iFood
IFOOD_WEBHOOK_SECRET = os.getenv("IFOOD_WEBHOOK_SECRET", "default_secret_change_me")

async def verify_signature(request: Request):
    """
    Valida a assinatura HMAC-SHA256 enviada pelo iFood.
    """
    signature = request.headers.get("x-ifood-signature")
    if not signature:
        raise HTTPException(status_code=403, detail="Assinatura ausente")

    body = await request.body()
    
    # Calcula o hash esperado
    expected_signature = hmac.new(
        IFOOD_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="Assinatura inválida")

@router.post("/ifood")
async def ifood_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _auth: None = Depends(verify_signature)
):
    """
    Endpoint para receber eventos do iFood (Inbound Webhook).
    Processa eventos de novos pedidos (PLACED) e mudanças de status.
    """
    try:
        payload = await request.json()
        
        # O iFood pode enviar uma lista de eventos ou um único evento
        events = payload if isinstance(payload, list) else [payload]
        
        for event in events:
            # Processamento assíncrono para não bloquear a resposta ao iFood
            # O iFood espera 200 OK rápido (< 3s)
            background_tasks.add_task(
                ifood_service.process_webhook_event,
                db,
                event
            )
            
        return {"status": "received"}
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Payload JSON inválido")
    except Exception as e:
        print(f"❌ Erro no Webhook iFood: {e}")
        # Retorna 200 para evitar retries infinitos do iFood em caso de erro de lógica interna
        # O erro deve ser tratado/logado internamente
        return {"status": "error_logged"}
