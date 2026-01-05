from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, PaymentProvider
from app.routers.auth import get_current_user
from app.services.payment.factory import PaymentFactory
from pydantic import BaseModel

router = APIRouter()

class PaymentConfigUpdate(BaseModel):
    marketplace_fee_percentage: float

@router.get("/auth-url/{provider}")
async def get_auth_url(
    provider: str,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """Gera o link para o usuário conectar sua conta (ex: MP)"""
    try:
        enum_provider = PaymentProvider(provider)
        service = PaymentFactory.get_provider(enum_provider)
        
        # O 'state' carrega o ID da empresa para segurança no callback
        state = str(current_user.id)
        url = await service.get_auth_url(state)
        
        return {"url": url}
    except ValueError:
        raise HTTPException(400, "Provedor inválido")

@router.post("/callback/{provider}")
async def oauth_callback(
    provider: str,
    code: str,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """Recebe o código do provedor e salva as credenciais"""
    try:
        enum_provider = PaymentProvider(provider)
        service = PaymentFactory.get_provider(enum_provider)
        
        # Troca code por tokens
        credentials = await service.exchange_code_for_token(code)
        
        # Salva no banco
        current_user.payment_provider = enum_provider
        current_user.payment_credentials = credentials
        db.commit()
        
        return {"message": "Conectado com sucesso!", "provider": provider}
    except Exception as e:
        raise HTTPException(400, f"Erro na conexão: {str(e)}")

@router.delete("/disconnect")
def disconnect_payment(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    current_user.payment_provider = PaymentProvider.NONE
    current_user.payment_credentials = None
    db.commit()
    return {"message": "Desconectado"}