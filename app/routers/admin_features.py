from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, AuditAction
from app.services.feature_flag_service import FeatureFlagService
from app.services.audit_service import AuditService
from app.routers.auth import get_current_user
from app.schemas import FeatureFlagUpdate

router = APIRouter()

@router.get("")
def list_my_features(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Retorna as flags da empresa atual."""
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    return FeatureFlagService.get_flags(db, company_id)

@router.post("")
def update_feature_flag(
    data: FeatureFlagUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Ativa/Desativa uma flag. 
    RESTRITO: Apenas se o usuário estiver em modo Impersonation (Suporte).
    """
    # Verifica se o usuário logado tem a flag de suporte (impersonator)
    is_support = getattr(current_user, "is_impersonator", False) 

    if not is_support:
        raise HTTPException(
            status_code=403, 
            detail="Apenas a equipe de suporte pode alterar funcionalidades Beta."
        )

    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id

    flag = FeatureFlagService.set_flag(db, company_id, data.key, data.is_enabled)

    # Auditoria Obrigatória
    AuditService.log(
        db, current_user, AuditAction.FEATURE_TOGGLE, "FeatureFlag", data.key,
        details={"enabled": data.is_enabled}, request=request
    )

    return {"message": f"Funcionalidade {data.key} atualizada.", "status": data.is_enabled}
