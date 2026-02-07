# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Company, Employee, UserRole
from app.schemas import DriverBalanceResponse, SettleDebtRequest
from app.routers.auth import get_current_user
from app.services.logistics_service import LogisticsService
from pydantic import BaseModel
from typing import List

router = APIRouter()

class LogisticsDashboard(BaseModel):
    active_drivers: int
    deliveries_today: int
    pending_deliveries: int
    average_delivery_time_minutes: int
    total_collected_cash: float
    top_driver: str | None

@router.get("/dashboard", response_model=LogisticsDashboard)
def get_logistics_dashboard(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    return LogisticsService.get_dashboard_data(db, str(company_id))

@router.get("/drivers")
def list_drivers(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Lista motoristas vinculados à empresa."""
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    return db.query(Employee).filter(
        Employee.company_id == company_id,
        Employee.role == "driver"
    ).all()

@router.get("/stats")
def get_logistics_stats(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Retorna estatísticas operacionais da frota."""
    # Placeholder para o dashboard de logística
    return {"active_drivers": 0, "pending_deliveries": 0}
