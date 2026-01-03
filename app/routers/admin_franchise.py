from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import date, datetime, time
from app.database import get_db
from app.models import Company, Order, OrderStatus, PaymentStatus
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

# Schemas locais para resposta (DTOs)
class StoreSummary(BaseModel):
    id: str
    name: str
    slug: str
    revenue: float
    orders: int

class FranchiseDashboard(BaseModel):
    total_revenue: float
    total_orders: int
    stores: List[StoreSummary]

@router.get("/dashboard", response_model=FranchiseDashboard)
def get_franchise_dashboard(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """
    Retorna a visão consolidada de todas as lojas pertencentes ao mesmo dono (email).
    """
    # 1. Validação de Acesso
    if not isinstance(current_user, Company):
        raise HTTPException(status_code=403, detail="Apenas proprietários podem acessar a visão de franquia")

    # 2. Identificar todas as lojas do grupo
    owner_email = current_user.owner_email
    companies = db.query(Company).filter(Company.owner_email == owner_email).all()
    
    if not companies:
        raise HTTPException(404, "Nenhuma loja encontrada")

    # 3. Definir período (Hoje)
    # Futuramente pode aceitar query params start_date/end_date
    today = date.today()
    start_dt = datetime.combine(today, time.min)
    end_dt = datetime.combine(today, time.max)

    # 4. Agregar dados
    stores_data = []
    global_revenue = 0.0
    global_orders = 0

    for company in companies:
        # Query de agregação por loja
        metrics = db.query(
            func.sum(Order.total_amount).label('revenue'),
            func.count(Order.id).label('count')
        ).filter(
            Order.company_id == company.id,
            Order.status != OrderStatus.CANCELED,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_dt,
            Order.created_at <= end_dt
        ).first()

        rev = float(metrics.revenue or 0)
        cnt = int(metrics.count or 0)

        stores_data.append({
            "id": str(company.id),
            "name": company.name,
            "slug": company.slug,
            "revenue": rev,
            "orders": cnt
        })

        global_revenue += rev
        global_orders += cnt

    # Ordenar por faturamento (Ranking)
    stores_data.sort(key=lambda x: x['revenue'], reverse=True)

    return {
        "total_revenue": global_revenue,
        "total_orders": global_orders,
        "stores": stores_data
    }