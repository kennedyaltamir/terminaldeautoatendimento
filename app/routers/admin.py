
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-09 18:15:00
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus, Company, OrderItem, PaymentStatus, ServiceRequest, Table, Product, Category, Employee
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, ServiceRequestResponse, ProductResponse, OrderPagination
from app.websockets import manager
from app.services.whatsapp_service import WhatsAppService
from app.services.loyalty_service import LoyaltyService
from app.services.webhook_dispatcher import WebhookDispatcher

router = APIRouter()
whatsapp_service = WhatsAppService()

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderPaymentUpdate(BaseModel):
    payment_status: PaymentStatus

def get_company_id(user: any) -> UUID:
    if isinstance(user, Company):
        return user.id
    if isinstance(user, Employee):
        return user.company_id
    raise HTTPException(status_code=403, detail="Usuário inválido")

@router.get("/{company_slug}/orders", response_model=List[OrderResponse])
def get_kitchen_orders(
    company_slug: str, 
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    user_slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug
    if user_slug != company_slug:
        raise HTTPException(status_code=403, detail="Sem permissão para esta empresa")

    company_id = get_company_id(current_user)

    orders = (
        db.query(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.items).selectinload(OrderItem.selected_options),
            selectinload(Order.table)
        )
        .filter(
            Order.company_id == company_id,
            Order.status.in_([OrderStatus.PENDING, OrderStatus.ACCEPTED, OrderStatus.PREPARING, OrderStatus.READY])
        )
        .order_by(Order.created_at.asc())
        .all()
    )
    
    # FIX: Retorna lista vazia [] em vez de 404 quando não há pedidos
    return orders

@router.get("/{company_slug}/orders/recent-completed", response_model=List[OrderResponse])
def get_recent_completed_orders(
    company_slug: str,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Retorna os últimos 10 pedidos finalizados para a função de Recall.
    """
    user_slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug
    if user_slug != company_slug:
        raise HTTPException(status_code=403, detail="Sem permissão")

    company_id = get_company_id(current_user)

    orders = (
        db.query(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.items).selectinload(OrderItem.selected_options),
            selectinload(Order.table)
        )
        .filter(
            Order.company_id == company_id,
            Order.status.in_([OrderStatus.DELIVERED, OrderStatus.CANCELED])
        )
        .order_by(Order.finished_at.desc())
        .limit(10)
        .all()
    )
    
    # FIX: Retorna lista vazia [] em vez de 404
    return orders

@router.get("/{company_slug}/history", response_model=OrderPagination)
def get_order_history(
    company_slug: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    user_slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug
    if user_slug != company_slug:
        raise HTTPException(status_code=403, detail="Sem permissão para esta empresa")

    company_id = get_company_id(current_user)

    query = db.query(Order).filter(Order.company_id == company_id)

    total = query.count()

    orders = (
        query
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.items).selectinload(OrderItem.selected_options),
            selectinload(Order.table)
        )
        .order_by(Order.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "data": orders,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.patch("/orders/{order_id}", status_code=200)
async def update_order_status(
    order_id: UUID,
    status_update: OrderStatusUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = get_company_id(current_user)

    # Carrega a empresa junto para ter acesso às configs de WhatsApp
    order = db.query(Order).options(
        selectinload(Order.table), 
        selectinload(Order.company)
    ).filter(
        Order.id == order_id,
        Order.company_id == company_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    old_status = order.status
    order.status = status_update.status

    if status_update.status in [OrderStatus.DELIVERED, OrderStatus.CANCELED]:
        order.finished_at = datetime.now()

    if status_update.status == OrderStatus.DELIVERED and order.payment_status == PaymentStatus.PAID:
        LoyaltyService.process_cashback(db, order)

    db.commit()

    # Gatilho de WhatsApp: Pedido Pronto
    if status_update.status == OrderStatus.READY and old_status != OrderStatus.READY:
        if order.customer_phone:
            table_num = str(order.table.table_number) if order.table else "Balcão"

            # Passa o objeto company para o serviço resolver a configuração correta
            background_tasks.add_task(
                whatsapp_service.notify_order_ready,
                customer_name=order.customer_name or "Cliente",
                phone=order.customer_phone,
                table_number=table_num,
                restaurant_name=order.company.name,
                company_settings=order.company
            )

    # Webhook Dispatch (Integração Externa)
    webhook_payload = {
        "id": str(order.id),
        "status": order.status,
        "old_status": old_status,
        "updated_at": str(datetime.now())
    }
    background_tasks.add_task(
        WebhookDispatcher.dispatch,
        "order.updated",
        webhook_payload,
        str(company_id)
    )

    table_num = order.table.table_number if order.table else "Delivery"
    user_slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug

    await manager.broadcast({
        "type": "order_update",
        "order_id": str(order.id),
        "status": order.status,
        "payment_status": order.payment_status,
        "table": table_num,
        "customer": order.customer_name
    }, user_slug)

    return {"message": "Status atualizado"}

@router.patch("/orders/{order_id}/payment", status_code=200)
async def update_order_payment(
    order_id: UUID,
    payment_update: OrderPaymentUpdate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    order = db.query(Order).filter(Order.id == order_id, Order.company_id == company_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    order.payment_status = payment_update.payment_status
    if payment_update.payment_status == PaymentStatus.PAID:
        LoyaltyService.process_cashback(db, order)

    db.commit()
    user_slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status, "payment_status": order.payment_status}, user_slug)
    return {"message": "Pagamento atualizado"}

# --- SERVICE REQUESTS (CHAMADOS DE GARÇOM) ---

@router.get("/{company_slug}/service-requests", response_model=List[ServiceRequestResponse])
def get_service_requests(
    company_slug: str,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Retorna chamados de garçom pendentes."""
    user_slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug
    if user_slug != company_slug:
        raise HTTPException(status_code=403, detail="Sem permissão")

    company_id = get_company_id(current_user)

    requests = db.query(ServiceRequest).join(Table).filter(
        ServiceRequest.company_id == company_id,
        ServiceRequest.status == "pending"
    ).order_by(ServiceRequest.created_at.asc()).all()

    # FIX: Retorna lista vazia [] em vez de 404 para não quebrar Promise.all no frontend
    return [
        {
            "id": r.id,
            "table_number": r.table.table_number,
            "service_type": r.service_type,
            "notes": r.notes,
            "status": r.status,
            "created_at": r.created_at
        }
        for r in requests
    ]

@router.patch("/service-requests/{request_id}/resolve", status_code=200)
def resolve_service_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Marca um chamado como resolvido."""
    company_id = get_company_id(current_user)

    req = db.query(ServiceRequest).filter(
        ServiceRequest.id == request_id,
        ServiceRequest.company_id == company_id
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")

    req.status = "resolved"
    db.commit()

    return {"message": "Chamado resolvido"}