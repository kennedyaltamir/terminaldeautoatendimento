from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Company, AuditLog, Employee, UserRole
from app.schemas import AuditLogResponse
from app.routers.auth import get_current_user

router = APIRouter()

def require_owner(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    # Gerentes também podem ver logs? Por enquanto, apenas Donos.
    raise HTTPException(status_code=403, detail="Acesso restrito ao proprietário")

@router.get("", response_model=List[AuditLogResponse])
def get_audit_logs(
    limit: int = 50,
    resource: Optional[str] = None,
    user_role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    """
    Lista os logs de auditoria da empresa.
    """
    query = db.query(AuditLog).filter(AuditLog.company_id == current_user.id)

    if resource:
        query = query.filter(AuditLog.resource == resource)
    
    if user_role:
        query = query.filter(AuditLog.user_role == user_role)

    return query.order_by(AuditLog.created_at.desc()).limit(limit).all()