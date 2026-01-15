# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 08:40:00
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus, Company, OrderType, OrderItem, Employee, UserRole, PaymentStatus, DriverLedger, LedgerType
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, DispatchOrderRequest, CompleteDeliveryRequest
from app.services.whatsapp_service import WhatsAppService
from app.websockets import manager
from datetime import datetime
from decimal import Decimal

router = APIRouter()
whatsapp_service = WhatsAppService()

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    return db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options)
    ).filter(
        Order.company_id == company_id,
        Order.order_type == OrderType.DELIVERY,
        Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
    ).order_by(Order.created_at.asc()).all()

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    background_tasks: BackgroundTasks,
    dispatch_data: Optional[DispatchOrderRequest] = Body(None),
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Marca o pedido como em rota de entrega. 
    O corpo da requisição é opcional para suportar despacho rápido.
    """
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    
    if not order: 
        raise HTTPException(404, "Pedido não encontrado")
    
    order.status = OrderStatus.DELIVERING
    
    if dispatch_data and dispatch_data.driver_id:
        order.driver_id = dispatch_data.driver_id
    
    db.commit()
    
    # Notificação assíncrona
    if order.customer_phone:
        background_tasks.add_task(
            whatsapp_service.notify_delivery_dispatch,
            customer_name=order.customer_name or "Cliente",
            phone=order.customer_phone,
            driver_name=None, # Pode ser expandido se houver relação com Employee
            order_id=str(order.id),
            slug=order.company.slug,
            company_settings=order.company
        )
    
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, order.company.slug)
    return {"message": "Pedido despachado"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_delivery(order_id: UUID, data: CompleteDeliveryRequest, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")
    
    order.status = OrderStatus.DELIVERED
    order.payment_status = PaymentStatus.PAID
    order.finished_at = datetime.now()
    db.commit()
    
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, "hamburgueria-ze")
    return {"message": "Entrega finalizada"}
