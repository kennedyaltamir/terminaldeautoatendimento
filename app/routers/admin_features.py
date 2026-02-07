# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 23:50:00
# DESCRIPTION: Router de Feature Flags - Normalizado para evitar 404 de trailing slash.
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, AuditAction
from app.services.feature_flag_service import FeatureFlagService
from app.services.audit_service import AuditService
from app.routers.auth import get_current_user
from app.schemas import FeatureFlagUpdate

# Definimos o router sem prefixo interno
router = APIRouter()

# 🛡️ FIX: Definimos a rota tanto para "" quanto para "/" para máxima compatibilidade
@router.get("")
@router.get("/")
def list_my_features(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Retorna as flags da empresa atual."""
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    return FeatureFlagService.get_flags(db, company_id)

@router.post("")
@router.post("/")
def update_feature_flag(
    data: FeatureFlagUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Ativa/Desativa uma flag. RESTRITO: Suporte (Impersonator)."""
    is_impersonator = getattr(current_user, "is_impersonator", False)
    if not is_impersonator:
        raise HTTPException(
            status_code=403, 
            detail="Operação permitida apenas para equipe de suporte técnico."
        )
    
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    flag = FeatureFlagService.set_flag(db, company_id, data.key, data.is_enabled)
    
    AuditService.log(
        db, current_user, AuditAction.FEATURE_TOGGLE, "FeatureFlag", data.key,
        details={"enabled": data.is_enabled, "target_company": str(company_id)}, 
        request=request
    )
    return {"message": f"Funcionalidade '{data.key}' atualizada.", "status": data.is_enabled}
