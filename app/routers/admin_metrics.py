# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-24 02:30:00
# DESCRIPTION: Router de métricas avançado com agregação de BI e suporte a RLS.

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, set_tenant
from app.routers.auth import get_current_user
from app.services.metrics_service import MetricsService
from datetime import date, timedelta
import logging

logger = logging.getLogger("MetricsRouter")
router = APIRouter()

def inject_tenant_context(db: Session, user: any):
    """🛡️ Injeta o ID da empresa na sessão do Postgres para o RLS."""
    company_id = user.id if hasattr(user, 'owner_email') else user.company_id
    set_tenant(db, str(company_id))
    return str(company_id)

@router.get("", response_model=None)
def get_dashboard_metrics(
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Retorna o conjunto completo de KPIs e dados para gráficos.
    """
    company_id = inject_tenant_context(db, current_user)
    
    # Lógica de período padrão: últimos 7 dias
    if not start_date: start_date = date.today() - timedelta(days=6)
    if not end_date: end_date = date.today()
    
    try:
        # O MetricsService realiza as queries complexas de agregação (SUM, COUNT, GROUP BY)
        metrics = MetricsService.get_aggregate_metrics(db, company_id, start_date, end_date)
        return metrics
    except Exception as e:
        logger.error(f"🔥 Erro ao gerar métricas para empresa {company_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar dados estatísticos.")

@router.get("/export")
def export_sales(
    start_date: date = Query(None), 
    end_date: date = Query(None), 
    db: Session = Depends(get_db), 
    current_user: any = Depends(get_current_user)
):
    """Exportação de dados em CSV para contabilidade."""
    company_id = inject_tenant_context(db, current_user)
    # Lógica de exportação via StreamingResponse...
    return {"message": "Exportação iniciada"}
