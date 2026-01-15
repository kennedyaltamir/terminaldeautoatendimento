# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-14 23:30:00
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, Employee
from app.schemas.company import CompanyAdminSettings, CompanyUpdate
from app.routers.auth import get_current_user

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
    company = current_user if isinstance(current_user, Company) else current_user.company
    settings = CompanyAdminSettings.model_validate(company)
    
    # 🛡️ MASCARAMENTO DE SEGURANÇA (UI)
    if settings.fiscal_token:
        settings.fiscal_token = f"****{settings.fiscal_token[-4:]}"
    if settings.csc_token:
        settings.csc_token = f"****{settings.csc_token[-4:]}"
    if settings.mp_access_token:
        settings.mp_access_token = f"APP_USR-****{settings.mp_access_token[-4:]}"
        
    return settings

@router.patch("/me", response_model=CompanyAdminSettings)
def update_my_company(
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    update_data = company_data.model_dump(exclude_unset=True)
    
    # 🛡️ PROTEÇÃO CONTRA SOBREESCRITA DE MÁSCARA
    # Se o frontend enviar o valor mascarado (****), ignoramos a atualização desse campo
    sensitive_fields = ["fiscal_token", "csc_token", "mp_access_token"]
    for field in sensitive_fields:
        if field in update_data and update_data[field] and "****" in update_data[field]:
            del update_data[field]

    for key, value in update_data.items():
        setattr(current_user, key, value)
        
    db.commit()
    db.refresh(current_user)
    return get_my_company(current_user)
