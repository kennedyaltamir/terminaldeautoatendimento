# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-20 01:20:00
import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models import Company, Employee, AuditAction
from app.schemas import (
    CompanyAdminSettings, 
    CompanyUpdate, 
    PasswordUpdate, 
    KioskValidationRequest
)
from app.routers.auth import get_current_user
from app.core.security import verify_password, get_password_hash
from app.services.audit_service import AuditService

router = APIRouter()
logger = logging.getLogger("CompanyRouter")

# --- CONSTANTES DE SEGURANÇA ---
MASK_PATTERN = "****"
MP_PREFIX = "APP_USR-"

# --- HELPERS PRIVADOS ---

def _apply_security_mask(token: Optional[str], prefix: str = "") -> Optional[str]:
    """Aplica máscara de ofuscação em strings sensíveis."""
    if not token:
        return None
    if len(token) <= 4:
        return f"{prefix}{MASK_PATTERN}"
    return f"{prefix}{MASK_PATTERN}{token[-4:]}"

def _is_masked(value: Any) -> bool:
    """Verifica se o valor recebido é uma máscara visual do frontend."""
    return isinstance(value, str) and MASK_PATTERN in value

# --- DEPENDÊNCIAS ---

def require_owner(current_user: Any = Depends(get_current_user)) -> Company:
    """Garante que o usuário logado seja o proprietário (Company)."""
    if isinstance(current_user, Company):
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acesso negado: Esta operação exige privilégios de proprietário."
    )

# --- ENDPOINTS ---

@router.get("/me", response_model=CompanyAdminSettings)
async def get_my_company(current_user: Any = Depends(get_current_user)):
    """
    Recupera o perfil do Tenant atual com ofuscação de segredos.
    Funciona para Owners e Employees (Staff).
    """
    company = current_user if isinstance(current_user, Company) else current_user.company
    
    settings = CompanyAdminSettings.model_validate(company)
    
    # Ofuscação de Tokens para trânsito seguro até a UI
    settings.mp_access_token = _apply_security_mask(settings.mp_access_token, MP_PREFIX)
    settings.whatsapp_token = _apply_security_mask(settings.whatsapp_token)
    
    # Status booleano para o Kiosk
    settings.kiosk_password_set = bool(company.kiosk_password_hash)
    
    return settings

@router.patch("/me", response_model=CompanyAdminSettings)
async def update_my_company(
    request: Request,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    """
    Atualiza configurações do estabelecimento com validação de integridade.
    Protege contra sobrescrita acidental de tokens mascarados.
    """
    update_dict = company_data.model_dump(exclude_unset=True)
    
    # 🛡️ GUARD: Proteção contra corrupção de segredos
    # Se o frontend enviar o valor mascarado (ex: APP_USR-****1234), nós ignoramos.
    for field in ["mp_access_token", "whatsapp_token"]:
        if field in update_dict:
            if _is_masked(update_dict[field]):
                del update_dict[field]
            elif update_dict[field] == "":
                update_dict[field] = None

    # Validação de formato para novos tokens Mercado Pago
    if update_dict.get("mp_access_token") and not update_dict["mp_access_token"].startswith(MP_PREFIX):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token inválido. Deve iniciar com {MP_PREFIX}"
        )

    # Gestão de Senha do Totem (Kiosk)
    if "kiosk_password" in update_dict:
        plain_pass = update_dict.pop("kiosk_password")
        if plain_pass:
            if len(plain_pass) < 4:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A senha do Totem deve ter no mínimo 4 dígitos."
                )
            current_user.kiosk_password_hash = get_password_hash(plain_pass)
        else:
            current_user.kiosk_password_hash = None

    # Auditoria: Captura estado anterior para o log
    old_data = {k: getattr(current_user, k) for k in update_dict.keys() if hasattr(current_user, k)}

    # Aplicação das mudanças
    for key, value in update_dict.items():
        setattr(current_user, key, value)
    
    try:
        db.commit()
        db.refresh(current_user)
        
        # Registro de Auditoria
        AuditService.log(
            db=db,
            user=current_user,
            action=AuditAction.UPDATE,
            resource="Company",
            resource_id=str(current_user.id),
            details={"changes": update_dict, "previous": old_data},
            request=request
        )
        
        return await get_my_company(current_user)
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erro ao atualizar empresa {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha interna ao persistir dados."
        )

@router.patch("/me/password", status_code=status.HTTP_200_OK)
async def update_password(
    request: Request,
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Altera a senha de acesso do usuário administrativo logado."""
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha atual informada está incorreta."
        )
    
    current_user.password_hash = get_password_hash(password_data.new_password)
    
    try:
        db.commit()
        AuditService.log(
            db=db,
            user=current_user,
            action=AuditAction.UPDATE,
            resource="UserPassword",
            resource_id=str(current_user.id),
            request=request
        )
        return {"message": "Senha alterada com sucesso."}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar credenciais.")

@router.post("/kiosk/validate", status_code=status.HTTP_200_OK)
async def validate_kiosk_password(
    data: KioskValidationRequest,
    current_user: Any = Depends(get_current_user)
):
    """
    Valida a senha de saída do modo Totem.
    Implementa fallback para '123456' se nenhuma senha customizada existir.
    """
    company = current_user if isinstance(current_user, Company) else current_user.company
    
    # Fallback para senha padrão de fábrica
    if not company.kiosk_password_hash:
        return {"valid": data.password == "123456"}
            
    # Validação criptográfica
    is_valid = verify_password(data.password, company.kiosk_password_hash)
    
    if not is_valid:
        logger.warning(f"Tentativa de desbloqueio de Kiosk falhou para o Tenant {company.slug}")
        
    return {"valid": is_valid}
