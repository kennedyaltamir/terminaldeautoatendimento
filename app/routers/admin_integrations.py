# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-07 00:35:00
"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.2.0 (RBAC & Tenant Fix)
 * DNA_ID: MF-ROUTER-INTEGRATIONS-V1-2
 * OBJETIVO: Router de Integrações com suporte a RBAC e resolução de Tenant.
 * CORREÇÃO: Permite acesso a gerentes e normaliza company_id.
 */
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union
from app.database import get_db
from app.models import Company, WebhookSubscription, Employee
from app.schemas import WebhookCreate, WebhookResponse
from app.routers.auth import get_current_user
import secrets

router = APIRouter()

# --- HELPERS DE SEGURANÇA E CONTEXTO ---

def get_company_id(user: Union[Company, Employee]) -> str:
    """Resolve o ID da empresa (UUID) independente do tipo de usuário."""
    if isinstance(user, Company):
        return str(user.id)
    return str(user.company_id)

def get_company_instance(user: Union[Company, Employee]) -> Company:
    """Retorna a instância da empresa."""
    if isinstance(user, Company):
        return user
    return user.company

def require_integration_access(current_user: Union[Company, Employee] = Depends(get_current_user)):
    """
    Permite acesso a Proprietários e Gerentes.
    """
    if isinstance(current_user, Company):
        return current_user
    
    allowed_roles = ['owner', 'manager', 'admin']
    role = str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role).lower()
    
    if role in allowed_roles:
        return current_user
        
    raise HTTPException(status_code=403, detail="Acesso restrito a gerentes e proprietários")

# --- WEBHOOKS ---

@router.get("/webhooks", response_model=List[WebhookResponse])
def list_webhooks(
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(require_integration_access)
):
    company_id = get_company_id(current_user)
    return db.query(WebhookSubscription).filter(WebhookSubscription.company_id == company_id).all()

@router.post("/webhooks", response_model=WebhookResponse, status_code=201)
def create_webhook(
    data: WebhookCreate,
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(require_integration_access)
):
    company_id = get_company_id(current_user)
    
    # Validar URL
    if not data.target_url.startswith("http"):
        raise HTTPException(400, "URL inválida")
        
    # Gerar segredo se não fornecido
    secret = data.secret or secrets.token_hex(24)
    
    webhook = WebhookSubscription(
        company_id=company_id,
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
    current_user: Union[Company, Employee] = Depends(require_integration_access)
):
    company_id = get_company_id(current_user)
    
    webhook = db.query(WebhookSubscription).filter(
        WebhookSubscription.id == webhook_id,
        WebhookSubscription.company_id == company_id
    ).first()
    
    if not webhook:
        raise HTTPException(404, "Webhook não encontrado")
        
    db.delete(webhook)
    db.commit()
    return None

# --- WHATSAPP ---

@router.get("/whatsapp/status")
def get_whatsapp_status(
    current_user: Union[Company, Employee] = Depends(require_integration_access)
):
    # Mock de status para evitar erro 404 no frontend se o serviço não estiver configurado
    return {"status": "disconnected", "message": "Serviço não configurado"}
