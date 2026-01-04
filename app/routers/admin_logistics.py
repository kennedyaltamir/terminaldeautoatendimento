from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from app.database import get_db
from app.models import Company, Employee, DriverLedger, LedgerType, UserRole, Order, OrderStatus, OrderType
from app.schemas import DriverBalanceResponse, SettleDebtRequest, DriverLedgerResponse
from app.routers.auth import get_current_user
from decimal import Decimal
from datetime import date, datetime, time
from pydantic import BaseModel

router = APIRouter()

# --- SCHEMAS ---

class LogisticsDashboard(BaseModel):
    active_drivers: int
    deliveries_today: int
    pending_deliveries: int
    average_delivery_time_minutes: int
    total_collected_cash: float
    top_driver: Optional[str] = None

def require_manager(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    if isinstance(current_user, Employee) and current_user.role in [UserRole.OWNER, UserRole.MANAGER]:
        return current_user
    raise HTTPException(status_code=403, detail="Acesso restrito a gerentes")

# --- ENDPOINTS ---

@router.get("/dashboard", response_model=LogisticsDashboard)
def get_logistics_dashboard(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_manager)
):
    """
    Retorna KPIs de logística em tempo real para o gestor da frota.
    """
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    today = date.today()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    # 1. Motoristas Ativos (Total cadastrado por enquanto, futuramente status online/offline)
    active_drivers = db.query(Employee).filter(
        Employee.company_id == company_id,
        Employee.role == UserRole.DRIVER,
        Employee.is_active == True
    ).count()

    # 2. Entregas Hoje
    deliveries_today = db.query(Order).filter(
        Order.company_id == company_id,
        Order.order_type == OrderType.DELIVERY,
        Order.status == OrderStatus.DELIVERED,
        Order.finished_at >= start_of_day,
        Order.finished_at <= end_of_day
    ).count()

    # 3. Entregas Pendentes (Fila)
    pending_deliveries = db.query(Order).filter(
        Order.company_id == company_id,
        Order.order_type == OrderType.DELIVERY,
        Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
    ).count()

    # 4. Tempo Médio de Entrega (Minutos)
    # Postgres: EXTRACT(EPOCH FROM (finished_at - created_at))
    avg_time_query = db.query(
        func.avg(func.extract('epoch', Order.finished_at - Order.created_at))
    ).filter(
        Order.company_id == company_id,
        Order.order_type == OrderType.DELIVERY,
        Order.status == OrderStatus.DELIVERED,
        Order.finished_at >= start_of_day
    ).scalar()
    
    avg_minutes = int(avg_time_query / 60) if avg_time_query else 0

    # 5. Total Arrecadado em Dinheiro (Cash Management)
    total_cash = db.query(func.sum(DriverLedger.amount)).filter(
        DriverLedger.company_id == company_id,
        DriverLedger.type == LedgerType.DEBT,
        DriverLedger.created_at >= start_of_day
    ).scalar() or Decimal(0)

    # 6. Top Driver (Quem mais entregou hoje)
    top_driver_query = db.query(
        Employee.name,
        func.count(Order.id).label('count')
    ).join(Order, Order.driver_id == Employee.id).filter(
        Order.company_id == company_id,
        Order.status == OrderStatus.DELIVERED,
        Order.finished_at >= start_of_day
    ).group_by(Employee.name).order_by(desc('count')).first()

    top_driver_name = top_driver_query.name if top_driver_query else None

    return {
        "active_drivers": active_drivers,
        "deliveries_today": deliveries_today,
        "pending_deliveries": pending_deliveries,
        "average_delivery_time_minutes": avg_minutes,
        "total_collected_cash": float(total_cash),
        "top_driver": top_driver_name
    }

@router.get("/drivers/{driver_id}/balance", response_model=DriverBalanceResponse)
def get_driver_balance(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_manager)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    driver = db.query(Employee).filter(
        Employee.id == driver_id,
        Employee.company_id == company_id,
        Employee.role == UserRole.DRIVER
    ).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    transactions = db.query(DriverLedger).filter(
        DriverLedger.driver_id == driver_id
    ).order_by(DriverLedger.created_at.desc()).limit(50).all()

    total_debt = db.query(func.sum(DriverLedger.amount)).filter(
        DriverLedger.driver_id == driver_id,
        DriverLedger.type == LedgerType.DEBT
    ).scalar() or Decimal(0)

    total_paid = db.query(func.sum(DriverLedger.amount)).filter(
        DriverLedger.driver_id == driver_id,
        DriverLedger.type.in_([LedgerType.PAYMENT, LedgerType.CREDIT])
    ).scalar() or Decimal(0)

    current_balance = total_debt - total_paid

    return {
        "driver_id": driver.id,
        "driver_name": driver.name,
        "current_debt": current_balance,
        "transactions": transactions
    }

@router.post("/drivers/{driver_id}/settle", status_code=200)
def settle_driver_debt(
    driver_id: int,
    data: SettleDebtRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_manager)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    driver = db.query(Employee).filter(
        Employee.id == driver_id,
        Employee.company_id == company_id
    ).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser positivo")

    ledger_entry = DriverLedger(
        company_id=company_id,
        driver_id=driver_id,
        type=LedgerType.PAYMENT,
        amount=data.amount,
        description=data.description
    )
    
    db.add(ledger_entry)
    db.commit()
    
    return {"message": "Pagamento registrado com sucesso"}