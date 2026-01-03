#app/routers/admin_delivery.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.database import get_db
from app.models import Order, OrderStatus, Company, OrderType, PaymentStatus, OrderItem, Employee, UserRole
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, DispatchOrderRequest
from app.services.whatsapp_service import WhatsAppService
from app.websockets import manager
from datetime import datetime

router = APIRouter()
whatsapp_service = WhatsAppService()

def require_delivery_access(current_user: any = Depends(get_current_user)):
    """
    Permite acesso se for o Dono (Company) ou um Funcionário (Employee).
    """
    # Se for Company (Dono), tem acesso total
    if hasattr(current_user, "owner_email"):
        return current_user
    
    # Se for Employee (Funcionário), tem acesso
    if hasattr(current_user, "role"):
        return current_user
        
    raise HTTPException(status_code=403, detail="Acesso negado: Tipo de usuário inválido")

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    # Identifica o ID da empresa
    if hasattr(current_user, "owner_email"):
        company_id = current_user.id
    else:
        company_id = current_user.company_id

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
    order_id: str,
    dispatch_data: DispatchOrderRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    if hasattr(current_user, "owner_email"):
        company_id = current_user.id
        slug = current_user.slug
    else:
        company_id = current_user.company_id
        # Busca slug da empresa se for funcionário
        company = db.query(Company).filter(Company.id == company_id).first()
        slug = company.slug if company else "unknown"

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == company_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    order.status = OrderStatus.DELIVERING
    
    # Atribuir Entregador
    if dispatch_data.driver_id:
        driver = db.query(Employee).filter(
            Employee.id == dispatch_data.driver_id,
            Employee.company_id == company_id,
            Employee.role == UserRole.DRIVER
        ).first()
        if not driver:
            raise HTTPException(status_code=400, detail="Entregador inválido")
        order.driver_id = driver.id

    db.commit()

    if order.customer_phone:
        msg = f"🛵 *Saiu para Entrega!* \n\nOlá {order.customer_name}, seu pedido está a caminho!"
        background_tasks.add_task(whatsapp_service.send_message, order.customer_phone, msg)

    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Pedido despachado"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_delivery(
    order_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    if hasattr(current_user, "owner_email"):
        company_id = current_user.id
        slug = current_user.slug
    else:
        company_id = current_user.company_id
        company = db.query(Company).filter(Company.id == company_id).first()
        slug = company.slug if company else "unknown"

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == company_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    order.status = OrderStatus.DELIVERED
    order.payment_status = PaymentStatus.PAID
    order.finished_at = datetime.now()
    db.commit()

    if order.customer_phone:
        msg = f"✅ *Pedido Entregue!* \n\nBom apetite, {order.customer_name}! 😋"
        background_tasks.add_task(whatsapp_service.send_message, order.customer_phone, msg)

    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Entrega finalizada"}