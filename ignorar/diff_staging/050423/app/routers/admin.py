# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 05:15:00
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List
from pydantic import BaseModel
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus, OrderItem, PaymentStatus, ServiceRequest, Table
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, ServiceRequestResponse
from app.services.order_service import OrderService

router = APIRouter()

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

@router.get("/{company_slug}/orders", response_model=List[OrderResponse])
def get_kitchen_orders(company_slug: str, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product), 
        selectinload(Order.table)
    ).filter(
        Order.company_id == company_id, 
        Order.status.in_([OrderStatus.PENDING, OrderStatus.ACCEPTED, OrderStatus.PREPARING, OrderStatus.READY])
    ).all()

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_admin(order_id: UUID, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    """Busca detalhes de um pedido específico (Admin)."""
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    order = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options),
        selectinload(Order.table)
    ).filter(Order.id == order_id, Order.company_id == company_id).first()
    
    if not order: 
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.patch("/orders/{order_id}", status_code=200)
async def update_order_status(order_id: UUID, status_update: OrderStatusUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    slug = current_user.slug if hasattr(current_user, 'owner_email') else current_user.company.slug
    order = await OrderService.update_status(db, order_id, status_update.status, slug, background_tasks)
    if not order: raise HTTPException(404, "Pedido não encontrado")
    return {"message": "Status atualizado"}

@router.get("/{company_slug}/service-requests", response_model=List[ServiceRequestResponse])
def get_service_requests(company_slug: str, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    requests = db.query(ServiceRequest).join(Table).filter(ServiceRequest.company_id == company_id, ServiceRequest.status == "pending").all()
    return [{"id": r.id, "table_number": r.table.table_number, "service_type": r.service_type, "notes": r.notes, "status": r.status, "created_at": r.created_at} for r in requests]
