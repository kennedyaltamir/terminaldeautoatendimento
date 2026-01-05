from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List
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

def require_delivery_access(current_user: any = Depends(get_current_user)):
    return current_user

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    orders = (
        db.query(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.items).selectinload(OrderItem.selected_options)
        )
        .filter(
            Order.company_id == company_id,
            Order.order_type == OrderType.DELIVERY,
            Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
        )
        .order_by(Order.created_at.asc())
        .all()
    )
    return orders

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    dispatch_data: DispatchOrderRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    slug = getattr(current_user, "slug", "unknown")
    if hasattr(current_user, "owner_email"): slug = current_user.slug

    # Carrega Company para pegar configs de WhatsApp
    order = db.query(Order).options(
        selectinload(Order.driver),
        selectinload(Order.company)
    ).filter(Order.id == order_id).first()

    if not order: raise HTTPException(404, "Pedido não encontrado")

    order.status = OrderStatus.DELIVERING
    if dispatch_data.driver_id:
        order.driver_id = dispatch_data.driver_id
        db.commit()
        db.refresh(order)

    # Gatilho de WhatsApp: Saiu para Entrega
    if order.customer_phone:
        background_tasks.add_task(
            whatsapp_service.notify_delivery_dispatch,
            customer_name=order.customer_name or "Cliente",
            phone=order.customer_phone,
            driver_name=order.driver.name if order.driver else None,
            order_id=str(order.id),
            slug=slug,
            company_settings=order.company # Injeção de dependência
        )

    db.commit()
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Pedido despachado"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_delivery(
    order_id: UUID,
    data: CompleteDeliveryRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    slug = getattr(current_user, "slug", "unknown")
    if hasattr(current_user, "owner_email"): slug = current_user.slug

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    if order.order_type == OrderType.DELIVERY:
        if order.delivery_code and order.delivery_code != data.code:
             if not data.code:
                 raise HTTPException(status_code=400, detail="Código de confirmação é obrigatório")
             raise HTTPException(status_code=403, detail="Código de confirmação incorreto")

    order.status = OrderStatus.DELIVERED
    order.payment_status = PaymentStatus.PAID
    order.finished_at = datetime.now()

    # Lógica de Ledger (Dívida do Motorista)
    # Se o pagamento for em dinheiro e tiver motorista, cria dívida
    if order.payment_method == "cash" and order.driver_id:
        ledger = DriverLedger(
            company_id=order.company_id,
            driver_id=order.driver_id,
            order_id=order.id,
            type=LedgerType.DEBT,
            amount=order.total_amount,
            description=f"Entrega #{str(order.id)[:6]}"
        )
        db.add(ledger)

    db.commit()

    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Entrega finalizada"}
