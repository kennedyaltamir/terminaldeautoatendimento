from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, cast, Date
from typing import List
from datetime import date, datetime, time, timedelta
from app.database import get_db
from app.models import Company, Order, OrderItem, ProductRecipe, Ingredient, OrderStatus, PaymentStatus
from app.routers.auth import get_current_user
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter()

class StoreSummary(BaseModel):
    id: str
    name: str
    slug: str
    revenue: float
    cmv: float
    fees: float
    profit: float
    margin_percent: float
    orders_count: int

class FranchiseDashboard(BaseModel):
    total_revenue: float
    total_profit: float
    avg_margin: float
    stores: List[StoreSummary]

@router.get("/dashboard", response_model=FranchiseDashboard)
def get_franchise_dashboard(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """
    Dashboard Multi-loja v2: Agregação de Receita, CMV e Lucratividade.
    Filtra por padrão as vendas do dia atual (UTC).
    """
    if not isinstance(current_user, Company):
        raise HTTPException(status_code=403, detail="Acesso restrito a proprietários")

    owner_email = current_user.owner_email
    companies = db.query(Company).filter(Company.owner_email == owner_email).all()

    if not companies:
        raise HTTPException(404, "Nenhuma loja encontrada")

    # Define o range de "Hoje" (Início e Fim do dia atual)
    today = date.today()
    start_dt = datetime.combine(today, time.min)
    # Estendemos o fim do dia para cobrir possíveis delays de timezone no banco
    end_dt = datetime.combine(today, time.max)

    stores_data = []
    global_revenue = Decimal("0.00")
    global_profit = Decimal("0.00")

    for company in companies:
        # 1. Agregação de Receita e Taxas
        order_metrics = db.query(
            func.sum(Order.total_amount).label('revenue'),
            func.sum(Order.service_fee).label('service_fees'),
            func.count(Order.id).label('count')
        ).filter(
            Order.company_id == company.id,
            Order.status != OrderStatus.CANCELED,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_dt,
            Order.created_at <= end_dt
        ).first()

        revenue = order_metrics.revenue or Decimal("0.00")
        service_fees = order_metrics.service_fees or Decimal("0.00")
        
        # 2. Cálculo de CMV Teórico (Baseado em Ficha Técnica)
        cmv_query = db.query(
            func.sum(OrderItem.quantity * ProductRecipe.quantity_required * Ingredient.cost_per_unit)
        ).join(Order, Order.id == OrderItem.order_id)\
         .join(ProductRecipe, ProductRecipe.product_id == OrderItem.product_id)\
         .join(Ingredient, Ingredient.id == ProductRecipe.ingredient_id)\
         .filter(
            Order.company_id == company.id,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_dt,
            Order.created_at <= end_dt
         ).scalar()

        cmv = Decimal(str(cmv_query or 0))
        
        # 3. Cálculo de Lucro Operacional
        profit = revenue - cmv - service_fees
        margin = (profit / revenue * 100) if revenue > 0 else 0

        stores_data.append(StoreSummary(
            id=str(company.id),
            name=company.name,
            slug=company.slug,
            revenue=float(revenue),
            cmv=float(cmv),
            fees=float(service_fees),
            profit=float(profit),
            margin_percent=float(margin),
            orders_count=int(order_metrics.count or 0)
        ))

        global_revenue += revenue
        global_profit += profit

    # Ordenar por Lucro (Melhores primeiro)
    stores_data.sort(key=lambda x: x.profit, reverse=True)

    avg_global_margin = (global_profit / global_revenue * 100) if global_revenue > 0 else 0

    return FranchiseDashboard(
        total_revenue=float(global_revenue),
        total_profit=float(global_profit),
        avg_margin=float(avg_global_margin),
        stores=stores_data
    )
