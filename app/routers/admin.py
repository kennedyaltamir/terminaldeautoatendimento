from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
import logging

from app.database import get_db, set_tenant
from app.models import Order, OrderStatus, OrderItem, Company, ServiceRequest, PaymentStatus, OrderType, OrderOrigin
from app.schemas import OrderResponse, OrderCreate, ServiceRequestResponse
from app.routers.auth import get_current_user
from app.services.order_service import OrderService

logger = logging.getLogger("AdminRouter")
router = APIRouter()

class OrderUpdatePayload(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[str] = None

# --- 1. ROTAS ESPECÍFICAS (PRIORIDADE MÁXIMA) ---

@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_admin_order(
    order_data: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    set_tenant(db, str(company_id))
    return await OrderService.create_order(db, company_id, order_data, "admin", OrderType.TAKEOUT, background_tasks)

@router.patch("/orders/{order_id}", status_code=200)
async def update_order_status(
    order_id: UUID, 
    payload: OrderUpdatePayload, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db), 
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    set_tenant(db, str(company_id))
    
    order = db.query(Order).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if payload.status:
        company = db.query(Company).filter(Company.id == company_id).first()
        await OrderService.update_status(db, order_id, payload.status, company.slug, company_id, background_tasks)
    
    if payload.payment_status:
        order.payment_status = payload.payment_status
        db.commit()
    return {"message": "OK"}

# --- 2. ROTAS DINÂMICAS (BASEADAS EM SLUG) ---

@router.get("/{company_slug}/orders", response_model=List[OrderResponse])
def get_kitchen_orders(
    company_slug: str, 
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    set_tenant(db, str(company_id))
    return db.query(Order).options(selectinload(Order.items).selectinload(OrderItem.product), selectinload(Order.table)).filter(
        Order.company_id == company_id,
        Order.status.in_([OrderStatus.PENDING, OrderStatus.ACCEPTED, OrderStatus.PREPARING, OrderStatus.READY])
    ).order_by(Order.created_at.asc()).all()

@router.get("/{company_slug}/service-requests", response_model=List[ServiceRequestResponse])
def get_service_requests(
    company_slug: str,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    set_tenant(db, str(company_id))
    return db.query(ServiceRequest).join(ServiceRequest.table).filter(
        ServiceRequest.company_id == company_id,
        ServiceRequest.status == "pending"
    ).order_by(ServiceRequest.created_at.asc()).all()

@router.patch("/{company_slug}/service-requests/{request_id}/resolve")
def resolve_service_request(
    company_slug: str,
    request_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    set_tenant(db, str(company_id))
    req = db.query(ServiceRequest).filter(ServiceRequest.id == request_id, ServiceRequest.company_id == company_id).first()
    if not req: raise HTTPException(status_code=404, detail="Não encontrado")
    req.status = "resolved"
    db.commit()
    return {"message": "Resolvido"}