# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 09:30:00

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from app.database import get_db
from app.models import Order, Company, OrderItem
from app.schemas import OrderPagination, OrderResponse
from app.routers.auth import get_current_user
from sqlalchemy import desc

router = APIRouter()

@router.get("/{company_slug}/history", response_model=OrderPagination)
def get_order_history(
    company_slug: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    # 1. Resolver Company ID pelo Slug
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    # 2. Validar Acesso (Se for funcionário, deve pertencer à empresa)
    if hasattr(current_user, "company_id") and str(current_user.company_id) != str(company.id):
        # Se for dono (Company object), verifica o ID direto
        if isinstance(current_user, Company) and str(current_user.id) != str(company.id):
             raise HTTPException(status_code=403, detail="Acesso negado a esta empresa")

    # 3. Construir Query
    query = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options),
        selectinload(Order.table)
    ).filter(Order.company_id == company.id)

    # Filtros
    if status:
        query = query.filter(Order.status == status)
    
    # Ordenação (Mais recentes primeiro)
    query = query.order_by(desc(Order.created_at))

    # 4. Paginação
    total = query.count()
    offset = (page - 1) * limit
    orders = query.offset(offset).limit(limit).all()

    return {
        "data": orders,
        "total": total,
        "page": page,
        "limit": limit
    }