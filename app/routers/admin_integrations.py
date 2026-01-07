from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Company, WebhookSubscription
from app.schemas import WebhookCreate, WebhookResponse
from app.routers.auth import get_current_user
import secrets

router = APIRouter()

def require_owner(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    raise HTTPException(status_code=403, detail="Acesso restrito ao proprietário")

@router.get("/webhooks", response_model=List[WebhookResponse])
def list_webhooks(
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    return db.query(WebhookSubscription).filter(WebhookSubscription.company_id == current_user.id).all()

@router.post("/webhooks", response_model=WebhookResponse, status_code=201)
def create_webhook(
    data: WebhookCreate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    # Validar URL
    if not data.target_url.startswith("http"):
        raise HTTPException(400, "URL inválida")

    # Gerar segredo se não fornecido (opcional no schema, mas obrigatório no model)
    secret = data.secret or secrets.token_hex(24)

    webhook = WebhookSubscription(
        company_id=current_user.id,
        target_url=data.target_url,
        events=data.events,
        secret=secret
    )
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook

@router.delete("/webhooks/{webhook_id}", status_code=204)
def delete_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    webhook = db.query(WebhookSubscription).filter(
        WebhookSubscription.id == webhook_id,
        WebhookSubscription.company_id == current_user.id
    ).first()

    if not webhook:
        raise HTTPException(404, "Webhook não encontrado")

    db.delete(webhook)
    db.commit()
    return None
