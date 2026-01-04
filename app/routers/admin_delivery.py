from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func, desc
from typing import List
from app.database import get_db
from app.models import Order, OrderStatus, Company, OrderType, PaymentStatus, OrderItem, Employee, UserRole, DriverLedger, LedgerType, PaymentMethod
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, DispatchOrderRequest, CompleteDeliveryRequest, DriverRecommendation
from app.services.whatsapp_service import WhatsAppService
from app.websockets import manager
from datetime import datetime
import os

router = APIRouter()
whatsapp_service = WhatsAppService()
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

def require_delivery_access(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    if isinstance(current_user, Employee):
        if current_user.role in [UserRole.OWNER, UserRole.MANAGER, UserRole.DRIVER]:
            return current_user
    raise HTTPException(status_code=403, detail="Acesso negado: Permissão insuficiente para Delivery")

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id

    # Agora retorna TODOS os status ativos de delivery, não apenas READY/DELIVERING
    orders = (
        db.query(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.items).selectinload(OrderItem.selected_options)
        )
        .filter(
            Order.company_id == company_id,
            Order.order_type == OrderType.DELIVERY,
            Order.status.in_([
                OrderStatus.PENDING, 
                OrderStatus.ACCEPTED, 
                OrderStatus.PREPARING, 
                OrderStatus.READY, 
                OrderStatus.DELIVERING
            ])
        )
        .order_by(Order.created_at.asc())
        .all()
    )
    return orders

@router.get("/recommendation", response_model=List[DriverRecommendation])
def get_driver_recommendation(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id

    drivers = db.query(Employee).filter(
        Employee.company_id == company_id,
        Employee.role == UserRole.DRIVER,
        Employee.is_active == True
    ).all()

    recommendations = []

    for driver in drivers:
        active_count = db.query(Order).filter(
            Order.driver_id == driver.id,
            Order.status == OrderStatus.DELIVERING
        ).count()

        last_delivery = db.query(Order).filter(
            Order.driver_id == driver.id,
            Order.status == OrderStatus.DELIVERED
        ).order_by(Order.finished_at.desc()).first()

        recommendations.append({
            "driver_id": driver.id,
            "name": driver.name,
            "active_deliveries": active_count,
            "last_delivery_time": last_delivery.finished_at if last_delivery else None
        })

    recommendations.sort(key=lambda x: (x["active_deliveries"], x["last_delivery_time"] or datetime.min))

    return recommendations

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: str,
    dispatch_data: DispatchOrderRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    if isinstance(current_user, Company):
        slug = current_user.slug
    else:
        company = db.query(Company).filter(Company.id == company_id).first()
        slug = company.slug if company else "unknown"

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == company_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Validação: Só pode despachar se estiver PRONTO
    if order.status not in [OrderStatus.READY]:
        raise HTTPException(status_code=400, detail="O pedido precisa ser finalizado pela cozinha antes de sair.")

    order.status = OrderStatus.DELIVERING
    
    if dispatch_data.driver_id:
        driver = db.query(Employee).filter(
            Employee.id == dispatch_data.driver_id,
            Employee.company_id == company_id,
            Employee.role == UserRole.DRIVER
        ).first()
        if not driver:
            raise HTTPException(status_code=400, detail="Entregador inválido")
        order.driver_id = driver.id
    
    elif isinstance(current_user, Employee) and current_user.role == UserRole.DRIVER:
        order.driver_id = current_user.id

    db.commit()

    if order.customer_phone:
        code_msg = ""
        if order.delivery_code:
            code_msg = f"\n🔑 *Seu código de entrega é: {order.delivery_code}*\nInforme ao entregador para receber o pedido."

        tracking_link = f"{FRONTEND_URL}/{slug}/menu?order={order.id}"
        
        msg = (
            f"🛵 *Saiu para Entrega!* \n\n"
            f"Olá {order.customer_name}, seu pedido está a caminho!\n"
            f"Acompanhe em tempo real: {tracking_link}"
            f"{code_msg}"
        )
        background_tasks.add_task(whatsapp_service.send_message, order.customer_phone, msg)

    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Pedido despachado"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_delivery(
    order_id: str,
    completion_data: CompleteDeliveryRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    if isinstance(current_user, Company):
        slug = current_user.slug
    else:
        company = db.query(Company).filter(Company.id == company_id).first()
        slug = company.slug if company else "unknown"

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == company_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.delivery_code:
        if not completion_data.code:
            raise HTTPException(status_code=400, detail="Código de confirmação obrigatório")
        if completion_data.code != order.delivery_code:
            raise HTTPException(status_code=403, detail="Código de confirmação incorreto")

    if order.payment_method == PaymentMethod.CASH and order.driver_id:
        if order.payment_status != PaymentStatus.PAID:
            ledger_entry = DriverLedger(
                company_id=company_id,
                driver_id=order.driver_id,
                order_id=order.id,
                type=LedgerType.DEBT,
                amount=order.total_amount,
                description=f"Entrega Pedido #{str(order.id)[:6]}"
            )
            db.add(ledger_entry)

    order.status = OrderStatus.DELIVERED
    order.payment_status = PaymentStatus.PAID
    order.finished_at = datetime.now()
    db.commit()

    if order.customer_phone:
        msg = f"✅ *Pedido Entregue!* \n\nBom apetite, {order.customer_name}! 😋"
        background_tasks.add_task(whatsapp_service.send_message, order.customer_phone, msg)

    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Entrega finalizada"}