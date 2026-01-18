# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-16 13:20:00
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, Employee, UserRole
from app.schemas import CompanyAdminSettings, CompanyUpdate, PasswordUpdate, KioskValidationRequest
from app.routers.auth import get_current_user
from app.core.security import verify_password, get_password_hash

router = APIRouter()

def require_owner(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    raise HTTPException(status_code=403, detail="Apenas o dono pode alterar configurações")

@router.get("/me", response_model=CompanyAdminSettings)
def get_my_company(current_user: any = Depends(get_current_user)):
    """
    Retorna os dados da empresa com mascaramento de credenciais sensíveis.
    """
    if isinstance(current_user, Employee):
        company = current_user.company
    else:
        company = current_user
    
    settings = CompanyAdminSettings.model_validate(company)
    
    # Mascaramento Mercado Pago
    if settings.mp_access_token:
        visible_part = settings.mp_access_token[-4:]
        settings.mp_access_token = f"APP_USR-****{visible_part}"
    
    # Mascaramento WhatsApp Token
    if settings.whatsapp_token:
        visible_part = settings.whatsapp_token[-4:]
        settings.whatsapp_token = f"****{visible_part}"
        
    # Kiosk Status
    settings.kiosk_password_set = bool(company.kiosk_password_hash)

    return settings

@router.patch("/me", response_model=CompanyAdminSettings)
def update_my_company(
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    update_data = company_data.model_dump(exclude_unset=True)
    
    # Lógica de Segurança para o Token MP
    if "mp_access_token" in update_data:
        token = update_data["mp_access_token"]
        if token == "": update_data["mp_access_token"] = None
        elif token and "****" in token: del update_data["mp_access_token"]
        elif token and not token.startswith("APP_USR-"):
            raise HTTPException(status_code=400, detail="Token do Mercado Pago inválido.")
            
    # Lógica de Segurança para o Token WhatsApp
    if "whatsapp_token" in update_data:
        token_ws = update_data["whatsapp_token"]
        if token_ws == "": update_data["whatsapp_token"] = None
        elif token_ws and "****" in token_ws: del update_data["whatsapp_token"]

    # Lógica de Senha do Kiosk (Hash)
    if "kiosk_password" in update_data:
        plain_pass = update_data.pop("kiosk_password")
        if plain_pass:
            if len(plain_pass) < 4:
                raise HTTPException(status_code=400, detail="Senha do Totem deve ter no mínimo 4 dígitos.")
            current_user.kiosk_password_hash = get_password_hash(plain_pass)
        else:
            # Se enviou string vazia, remove a senha (volta pro default 123456 na lógica de validação se quiser, ou desativa)
            # Decisão: Se remover, fica sem senha customizada, usa default.
            current_user.kiosk_password_hash = None

    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    # Retorna mascarado
    settings = CompanyAdminSettings.model_validate(current_user)
    if settings.mp_access_token:
        settings.mp_access_token = f"APP_USR-****{settings.mp_access_token[-4:]}"
    if settings.whatsapp_token:
        settings.whatsapp_token = f"****{settings.whatsapp_token[-4:]}"
    settings.kiosk_password_set = bool(current_user.kiosk_password_hash)
    
    return settings

@router.patch("/me/password", status_code=status.HTTP_200_OK)
def update_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
    
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Senha alterada com sucesso"}

@router.post("/kiosk/validate", status_code=status.HTTP_200_OK)
def validate_kiosk_password(
    data: KioskValidationRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Valida a senha do Kiosk.
    Se não houver senha configurada, aceita '123456' como fallback.
    """
    # Identifica a empresa
    company = current_user if isinstance(current_user, Company) else current_user.company
    
    # Fallback Default
    if not company.kiosk_password_hash:
        if data.password == "123456":
            return {"valid": True}
        else:
            return {"valid": False}
            
    # Validação Real
    if verify_password(data.password, company.kiosk_password_hash):
        return {"valid": True}
        
    return {"valid": False}

