# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 14:40:00
import math
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, selectinload
from typing import List, Any
from uuid import UUID
from datetime import datetime
from app.database import get_db
from app.models import Order, OrderStatus, Employee
from app.routers.auth import get_current_user
from app.websockets import manager

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
        Order.status.in_(["ready", "delivering"])
    ).order_by(Order.created_at.desc()).all()

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Inicia a entrega com Event Adapter para Cliente e Driver."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    driver_id = current_user.id if isinstance(current_user, Employee) else None
    
    order = db.query(Order).with_for_update().options(selectinload(Order.company)).filter(
        Order.id == order_id, 
        Order.company_id == company_id
    ).first()

    if not order: 
        raise HTTPException(404, "Pedido não encontrado")

    # Idempotência
    if order.status == "delivering" and order.driver_id == driver_id:
        return {"message": "Rota já iniciada", "status": "delivering"}

    order.status = "delivering"
    order.driver_id = driver_id
    db.commit()

    # 🛡️ EVENT ADAPTER (L9): Emite para ambos os contextos
    # 1. Contexto Técnico (Driver/Admin)
    await manager.broadcast({
        "type": "delivery.status", 
        "order_id": str(order.id), 
        "status": "delivering"
    }, order.company.slug)

    # 2. Contexto de Domínio (Cliente) - CORREÇÃO DA CEGUEIRA
    await manager.broadcast({
        "type": "order_update",
        "order_id": str(order.id),
        "status": "delivering"
    }, order.company.slug)

    return {"message": "Rota iniciada", "status": "delivering"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    order.status = "delivered"
    order.finished_at = datetime.now()
    db.commit()

    # Notificação Normalizada
    await manager.broadcast({
        "type": "order_update",
        "order_id": str(order.id),
        "status": "delivered"
    }, order.company.slug)

    return {"message": "Entrega finalizada", "status": "delivered"}

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
    
    dest_lat, dest_lng = -19.22815, -44.94195
    eta_seconds = calculate_eta_simple(lat, lng, dest_lat, dest_lng)

    # 🛡️ EVENT ADAPTER (L9): Normalização de Telemetria
    # O Cliente espera "DELIVERY_LOCATION" com payload aninhado
    await manager.broadcast({
        "type": "DELIVERY_LOCATION",
        "order_id": str(order.id),
        "payload": {
            "lat": lat,
            "lng": lng,
            "eta_seconds": eta_seconds
        }
    }, order.company.slug)

    return {"status": "propagated", "eta_seconds": eta_seconds}

