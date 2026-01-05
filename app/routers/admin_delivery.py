
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.database import get_db
from app.models import Order, OrderStatus, Company, OrderType, OrderItem, Employee, UserRole
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, DispatchOrderRequest
from app.services.whatsapp_service import WhatsAppService
from app.websockets import manager
from datetime import datetime

router = APIRouter()
whatsapp_service = WhatsAppService()

def require_delivery_access(current_user: any = Depends(get_current_user)):
    print(f"\n🔍 [DEBUG AUTH] Usuário autenticado: {current_user}")
    print(f"   Tipo: {type(current_user)}")
    
    # Tenta listar atributos para debug
    try:
        if hasattr(current_user, '__dict__'):
            print(f"   Atributos: {current_user.__dict__.keys()}")
    except:
        pass

    # Lógica Permissiva: Se chegou aqui, está logado.
    return current_user

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    print("🚀 [DEBUG ROUTE] Entrou em GET /orders")
    
    # Tenta descobrir o ID da empresa de qualquer jeito
    company_id = None
    
    # Caso 1: É o Dono (Company)
    if hasattr(current_user, "owner_email"):
        company_id = current_user.id
        print("   -> Identificado como DONO")
        
    # Caso 2: É Funcionário (Employee)
    elif hasattr(current_user, "role"):
        company_id = current_user.company_id
        print("   -> Identificado como FUNCIONÁRIO")
        
    # Caso 3: Fallback genérico
    if not company_id:
        company_id = getattr(current_user, "id", None)
        print("   -> Fallback ID usado")

    print(f"   -> Company ID alvo: {company_id}")

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
    
    print(f"✅ [DEBUG DB] Retornando {len(orders)} pedidos")
    return orders

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: str,
    dispatch_data: DispatchOrderRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    print(f"🚀 [DEBUG] Despachando {order_id}")
    
    # Lógica simplificada de ID
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    slug = getattr(current_user, "slug", "unknown")
    if hasattr(current_user, "owner_email"): slug = current_user.slug

    order = db.query(Order).filter(Order.id == order_id).first() # Simplificado para teste
    
    if not order: raise HTTPException(404, "Pedido não encontrado")

    order.status = OrderStatus.DELIVERING
    if dispatch_data.driver_id:
        order.driver_id = dispatch_data.driver_id

    db.commit()
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Despachado"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_delivery(
    order_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    print(f"✅ [DEBUG] Finalizando {order_id}")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    order.status = OrderStatus.DELIVERED
    order.payment_status = PaymentStatus.PAID
    order.finished_at = datetime.now()
    db.commit()
    
    slug = getattr(current_user, "slug", "unknown")
    if hasattr(current_user, "owner_email"): slug = current_user.slug
    
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, slug)
    return {"message": "Finalizado"}
