# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 13:50:00
import math
from fastapi import APIRouter, Depends, HTTPException, Body, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from typing import List, Any
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus, Employee
from app.routers.auth import get_current_user
from app.websockets import manager
from app.services.order_service import OrderService

router = APIRouter()

def calculate_eta_simple(curr_lat: float, curr_lng: float, dest_lat: float, dest_lng: float) -> int:
    """Enterprise ETA Model (Haversine)."""
    R = 6371000.0
    phi1 = math.radians(curr_lat)
    phi2 = math.radians(dest_lat)
    dphi = math.radians(dest_lat - curr_lat)
    dlambda = math.radians(dest_lng - curr_lng)
    a = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_meters = R * c
    if distance_meters <= 0: return 60
    speed_mps = 5.5 
    return int((distance_meters / speed_mps) * 1.25)

@router.get("/orders", response_model=None)
def get_delivery_orders(db: Session = Depends(get_db), current_user: Any = Depends(get_current_user)):
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    return db.query(Order).filter(
        Order.company_id == company_id,
        Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
    ).order_by(Order.created_at.desc()).all()

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Inicia a entrega com LOCK TRANSACIONAL e IDEMPOTÊNCIA."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    driver_id = current_user.id if isinstance(current_user, Employee) else None
    
    order = db.query(Order).with_for_update().options(selectinload(Order.company)).filter(
        Order.id == order_id, 
        Order.company_id == company_id
    ).first()
    
    if not order: 
        raise HTTPException(404, "Pedido não encontrado")

    if order.status == OrderStatus.DELIVERING:
        if order.driver_id == driver_id:
            return {"message": "Rota já iniciada (Idempotent)", "status": "delivering"}
        else:
            raise HTTPException(400, "Este pedido já foi coletado por outro entregador.")

    if order.status != OrderStatus.READY:
        raise HTTPException(400, "Pedido ainda não está pronto para entrega.")

    order.status = OrderStatus.DELIVERING
    order.driver_id = driver_id
    db.commit()
    
    await manager.broadcast({
        "type": "delivery.status", 
        "payload": {"order_id": str(order.id), "status": "delivering"}
    }, order.company.slug)
    
    return {"message": "Rota iniciada", "status": "delivering"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_delivery(
    order_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Finaliza a entrega e dispara o ciclo de fidelidade/notificações."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(
        Order.id == order_id, 
        Order.company_id == company_id
    ).first()
    
    if not order: 
        raise HTTPException(404, "Pedido não encontrado")
    
    if order.status == OrderStatus.DELIVERED:
        return {"message": "Entrega já finalizada"}

    # Utiliza o Service para garantir consistência de eventos (Loyalty, WS)
    await OrderService.update_status(db, order_id, OrderStatus.DELIVERED, order.company.slug, background_tasks)
    
    return {"message": "Entrega finalizada com sucesso"}

@router.post("/orders/{order_id}/location", status_code=200)
async def update_order_location(
    order_id: UUID,
    lat: float = Body(..., embed=True),
    lng: float = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")
    if isinstance(current_user, Employee) and order.driver_id != current_user.id:
        raise HTTPException(403, "Você não é o entregador deste pedido.")
    
    await manager.broadcast({
        "type": "delivery.location",
        "payload": {
            "order_id": str(order.id),
            "lat": lat,
            "lng": lng
        }
    }, order.company.slug)
    return {"status": "propagated"}
