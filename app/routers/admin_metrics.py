
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, Employee, UserRole
from app.schemas import DashboardMetrics, TopProduct
from app.routers.auth import get_current_user
from app.services.metrics_service import MetricsService
from datetime import date, timedelta

router = APIRouter()

@router.get("", response_model=DashboardMetrics)
def get_dashboard_metrics(
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    if not start_date: start_date = date.today() - timedelta(days=6)
    if not end_date: end_date = date.today()
    
    data = MetricsService.get_aggregate_metrics(db, str(company_id), start_date, end_date)
    
    # Map top products for schema compatibility
    top_products = [
        TopProduct(name=p["name"], count=p["quantity"], revenue=p["revenue"]) 
        for p in data["product_performance"][:5]
    ]
    
    return {
        "total_revenue": data["total_revenue"],
        "total_orders": data["total_orders"],
        "average_ticket": data["average_ticket"],
        "top_products": top_products,
        "sales_chart": data["sales_chart"],
        "sales_by_hour": data["sales_by_hour"],
        "product_performance": data["product_performance"],
        "ticket_evolution": [] # Placeholder for future expansion
    }

