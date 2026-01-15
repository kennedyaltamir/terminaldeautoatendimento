# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 11:15:00
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus, Company, OrderType, OrderItem, Employee, UserRole, PaymentStatus
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, DispatchOrderRequest, CompleteDeliveryRequest
from app.websockets import manager
from datetime import datetime

router = APIRouter()

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.table)
    ).filter(
        Order.company_id == company_id,
        Order.order_type == OrderType.DELIVERY,
        Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
    ).order_by(Order.created_at.asc()).all()

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    dispatch_data: Optional[DispatchOrderRequest] = Body(None),
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Inicia a entrega e notifica o cliente."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")
    
    order.status = OrderStatus.DELIVERING
    db.commit()
    
    await manager.broadcast({
        "type": "order_update", 
        "order_id": str(order.id), 
        "status": "delivering",
        "customer_name": order.customer_name
    }, order.company.slug)
    
    return {"message": "Rota iniciada"}

@router.post("/orders/{order_id}/location", status_code=200)
async def update_order_location(
    order_id: UUID,
    lat: float = Body(..., embed=True),
    lng: float = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Propaga a localização GPS do entregador em tempo real."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    await manager.broadcast({
        "type": "driver_location",
        "order_id": str(order.id),
        "lat": lat,
        "lng": lng
    }, order.company.slug)
    
    return {"status": "broadcast_ok"}
