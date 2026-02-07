# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-23 05:05:00
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from app.database import get_db
from app.models import Order, Company, OrderItem
from app.schemas import OrderPagination
from app.routers.auth import get_current_user
from sqlalchemy import desc

router = APIRouter()

@router.get("", response_model=OrderPagination)
def get_order_history(
    slug: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    # 1. Identificar a empresa (pelo slug ou pelo token do usuário)
    company_id = None
    if slug:
        company = db.query(Company).filter(Company.slug == slug).first()
        if not company: raise HTTPException(404, "Empresa não encontrada")
        company_id = company.id
    else:
        company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id

    # 2. Validar Acesso
    if hasattr(current_user, "company_id") and str(current_user.company_id) != str(company_id):
        raise HTTPException(403, "Acesso negado")

    # 3. Query
    query = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.table)
    ).filter(Order.company_id == company_id)

    if status: query = query.filter(Order.status == status)
    
    total = query.count()
    orders = query.order_by(desc(Order.created_at)).offset((page - 1) * limit).limit(limit).all()

    return {
        "data": orders,
        "total": total,
        "page": page,
        "limit": limit
    }