
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Company, Employee, UserRole
from app.schemas import DriverBalanceResponse, SettleDebtRequest
from app.routers.auth import get_current_user
from app.services.logistics_service import LogisticsService
from pydantic import BaseModel

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

