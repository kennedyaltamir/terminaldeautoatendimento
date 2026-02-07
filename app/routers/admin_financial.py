# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import Company, ServiceFeeLedger, Employee
from app.schemas import TipReportItem
from app.routers.auth import get_current_user
from datetime import date, datetime, time

router = APIRouter()

def require_manager(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    if hasattr(current_user, "role") and current_user.role in ["manager", "owner"]:
        return current_user
    raise HTTPException(status_code=403, detail="Acesso restrito a gerentes")

@router.get("/tips", response_model=List[TipReportItem])
def get_tips_report(
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: any = Depends(require_manager)
):
    """
    Relatório de Gorjetas por Funcionário.
    """
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    if not start_date: start_date = date.today()
    if not end_date: end_date = date.today()
    
    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)

    # Agregação SQL
    results = db.query(
        Employee.name,
        func.sum(ServiceFeeLedger.amount).label("total_tips"),
        func.count(ServiceFeeLedger.id).label("order_count")
    ).join(ServiceFeeLedger, Employee.id == ServiceFeeLedger.employee_id)\
     .filter(
         ServiceFeeLedger.company_id == company_id,
         ServiceFeeLedger.created_at >= start_dt,
         ServiceFeeLedger.created_at <= end_dt
     )\
     .group_by(Employee.name)\
     .all()

    return [
        {
            "employee_name": row.name,
            "total_tips": float(row.total_tips or 0),
            "order_count": row.order_count
        }
        for row in results
    ]