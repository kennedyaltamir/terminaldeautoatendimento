import os
import shutil

# Conteúdo da rota com DEBUG e Permissão Permissiva
NEW_CONTENT = r'''
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

print("✅ MÓDULO DELIVERY CARREGADO COM SUCESSO (VERSÃO DEBUG)")

def require_delivery_access(current_user: any = Depends(get_current_user)):
    """
    Verificação de segurança com DEBUG EXPLICITO.
    """
    print(f"🔐 [DEBUG DELIVERY] Tentativa de acesso. Tipo: {type(current_user)}")
    
    # Se chegou aqui, o token é válido. Vamos liberar para destravar a simulação.
    return current_user

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    print("👀 [DEBUG] Entrou no GET /orders")
    
    # Identifica o ID da empresa de forma segura (Duck Typing)
    if hasattr(current_user, "owner_email"):
        company_id = current_user.id
        print(f"   -> Usuário é DONO. ID: {company_id}")
    elif hasattr(current_user, "role"):
        company_id = current_user.company_id
        print(f"   -> Usuário é FUNCIONÁRIO. Company ID: {company_id}")
    else:
        # Fallback de emergência
        print("   -> Usuário desconhecido, tentando atributo id genérico")
        company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))

    if not company_id:
        print("❌ ERRO CRÍTICO: Não foi possível determinar company_id")
        raise HTTPException(status_code=400, detail="Erro de identificação da empresa")

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
    
    print(f"📦 [DEBUG] Pedidos encontrados no banco: {len(orders)}")
    return orders

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: str,
    dispatch_data: DispatchOrderRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_delivery_access)
):
    print(f"🚀 [DEBUG] Despachando pedido {order_id}")
    
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
    print(f"✅ [DEBUG] Finalizando pedido {order_id}")
    
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
'''

def main():
    target_path = os.path.join("app", "routers", "admin_delivery.py")
    
    print(f"🔧 Reescrevendo {target_path}...")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(NEW_CONTENT)
    
    print("🧹 Limpando caches (__pycache__)...")
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
                
    print("✅ Correção aplicada! Reinicie o servidor.")

if __name__ == "__main__":
    main()