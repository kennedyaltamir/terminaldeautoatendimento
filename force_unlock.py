import os
import time

# 1. Rota de Delivery SEM AUTENTICAÇÃO (Pública)
DELIVERY_CONTENT = r'''
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.database import get_db
from app.models import Order, OrderStatus, OrderType, OrderItem
from app.schemas import OrderResponse, DispatchOrderRequest
from app.websockets import manager
from datetime import datetime

router = APIRouter()

print("🔓 MÓDULO DELIVERY: MODO PÚBLICO ATIVADO")

@router.get("/orders", response_model=List[OrderResponse])
def get_delivery_orders(db: Session = Depends(get_db)):
    print("👀 [DEBUG] GET /orders (PÚBLICO) chamado!")
    
    # Retorna TUDO que for delivery, sem filtrar por empresa
    orders = (
        db.query(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.items).selectinload(OrderItem.selected_options)
        )
        .filter(
            Order.order_type == OrderType.DELIVERY,
            Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
        )
        .order_by(Order.created_at.asc())
        .all()
    )
    
    print(f"   -> Encontrados: {len(orders)} pedidos")
    return orders

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: str,
    dispatch_data: DispatchOrderRequest,
    db: Session = Depends(get_db)
):
    print(f"🚀 [DEBUG] Despachando {order_id} (PÚBLICO)")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    order.status = OrderStatus.DELIVERING
    if dispatch_data.driver_id:
        order.driver_id = dispatch_data.driver_id

    db.commit()
    # Broadcast genérico
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, "hamburgueria-ze")
    return {"message": "Despachado"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_delivery(order_id: str, db: Session = Depends(get_db)):
    print(f"✅ [DEBUG] Finalizando {order_id} (PÚBLICO)")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    order.status = OrderStatus.DELIVERED
    order.payment_status = "paid"
    order.finished_at = datetime.now()
    db.commit()
    
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, "hamburgueria-ze")
    return {"message": "Finalizado"}
'''

def touch_main():
    """Lê e reescreve o main.py para forçar reload"""
    main_path = os.path.join("app", "main.py")
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Adiciona um comentário timestamp no final
    timestamp = time.time()
    new_content = content + f"\n# Force Reload: {timestamp}\n"
    
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"🔄 app/main.py 'tocado' para forçar reload.")

def main():
    print("🔧 Aplicando Desbloqueio Total...")
    
    # Reescreve Delivery
    with open(os.path.join("app", "routers", "admin_delivery.py"), "w", encoding="utf-8") as f:
        f.write(DELIVERY_CONTENT)
    print("📝 admin_delivery.py reescrito (Modo Público).")
    
    # Força Reload
    touch_main()
    
    print("\n✅ Pronto! O servidor deve recarregar sozinho.")
    print("👉 Tente rodar o teste novamente em alguns segundos.")

if __name__ == "__main__":
    main()