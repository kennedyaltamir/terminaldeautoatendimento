# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-09 00:30:00
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, time
import csv
import io

from app.database import get_db
from app.models import Company, AuditLog
from app.schemas import AuditLogResponse
from app.routers.auth import get_current_user

router = APIRouter()

def require_owner(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    # Em um cenário real, poderíamos permitir que gerentes de segurança vissem,
    # mas por padrão Enterprise, apenas o Dono (Owner) tem acesso a auditoria completa.
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
    Lista os logs de auditoria da empresa (Paginado/Visualização).
    """
    query = db.query(AuditLog).filter(AuditLog.company_id == current_user.id)

    if resource:
        query = query.filter(AuditLog.resource == resource)

    if user_role:
        query = query.filter(AuditLog.user_role == user_role)

    return query.order_by(AuditLog.created_at.desc()).limit(limit).all()

@router.get("/export", response_class=StreamingResponse)
def export_audit_logs(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    """
    Exporta logs de auditoria em formato CSV para ingestão em SIEM ou arquivamento.
    Utiliza StreamingResponse para eficiência de memória.
    """
    query = db.query(AuditLog).filter(AuditLog.company_id == current_user.id)

    if start_date:
        dt_start = datetime.combine(start_date, time.min)
        query = query.filter(AuditLog.created_at >= dt_start)
    
    if end_date:
        dt_end = datetime.combine(end_date, time.max)
        query = query.filter(AuditLog.created_at <= dt_end)

    # Ordenação cronológica para exportação
    query = query.order_by(AuditLog.created_at.asc())

    def iter_csv():
        # Buffer de memória para escrita CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # Escreve Header
        writer.writerow(["Timestamp", "Actor", "Role", "Action", "Resource", "Resource ID", "IP Address", "Details"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        # Itera sobre os resultados (Yield per row/batch)
        # Em produção com muitos dados, idealmente usaríamos yield_per do SQLAlchemy
        for log in query.yield_per(1000):
            writer.writerow([
                log.created_at.isoformat(),
                log.user_name,
                log.user_role,
                log.action,
                log.resource,
                log.resource_id,
                log.ip_address or "N/A",
                str(log.details) if log.details else ""
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    filename = f"audit_logs_{current_user.slug}_{date.today()}.csv"
    
    return StreamingResponse(
        iter_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
