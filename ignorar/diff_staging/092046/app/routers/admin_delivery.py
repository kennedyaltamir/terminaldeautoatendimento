# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 15:20:00
import math
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, selectinload
from typing import List, Any, Optional
from uuid import UUID
from datetime import datetime
from app.database import get_db
from app.models import Order, OrderStatus, Employee
from app.routers.auth import get_current_user
from app.websockets import manager

router = APIRouter()

def calculate_eta_simple(curr_lat: float, curr_lng: float, dest_lat: float, dest_lng: float) -> int:
    """Enterprise ETA Model (Haversine + Traffic Buffer)."""
    R = 6371000.0
    phi1, phi2 = math.radians(curr_lat), math.radians(dest_lat)
    dphi = math.radians(dest_lat - curr_lat)
    dlambda = math.radians(dest_lng - curr_lng)

    a = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_meters = R * c

    if distance_meters <= 0: return 60
    speed_mps = 5.5 # ~20km/h
    eta_seconds = int((distance_meters / speed_mps) * 1.25)
    return max(60, eta_seconds)

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
    """Inicia a entrega com LOCK TRANSACIONAL REAL."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    # 🛡️ TYPE SAFETY: Company ID is UUID, Employee ID is INT. driver_id expects INT.
    driver_id = current_user.id if isinstance(current_user, Employee) else None
    
    if driver_id:
        active_job = db.query(Order).with_for_update().filter(
            Order.driver_id == driver_id, 
            Order.status == OrderStatus.DELIVERING
        ).first()
        if active_job:
            raise HTTPException(400, "Você já possui uma entrega em andamento.")

    order = db.query(Order).with_for_update().options(selectinload(Order.company)).filter(
        Order.id == order_id, 
        Order.company_id == company_id
    ).first()
    
    if not order: raise HTTPException(404, "Pedido não encontrado")
    if order.status != OrderStatus.READY:
        raise HTTPException(400, "Pedido já coletado ou não está pronto.")

    order.status = OrderStatus.DELIVERING
    order.driver_id = driver_id
    db.commit()
    
    await manager.broadcast({
        "type": "order_update", 
        "order_id": str(order.id), 
        "status": "delivering"
    }, order.company.slug)
    return {"message": "Rota iniciada"}

@router.post("/orders/{order_id}/location", status_code=200)
async def update_order_location(
    order_id: UUID,
    lat: float = Body(..., embed=True),
    lng: float = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Atualiza localização e propaga via WS v2."""
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    # Bypass para testes com conta Admin (Company) ou validação de Driver
    if isinstance(current_user, Employee) and order.driver_id != current_user.id:
        raise HTTPException(403, "Você não é o entregador deste pedido.")
    
    dest_lat, dest_lng = -19.22815, -44.94195
    eta_seconds = calculate_eta_simple(lat, lng, dest_lat, dest_lng)

    await manager.broadcast({
        "type": "DELIVERY_LOCATION",
        "payload": {
            "order_id": str(order.id),
            "lat": lat,
            "lng": lng,
            "eta_seconds": eta_seconds
        },
        "v": 2
    }, order.company.slug)
    
    return {"status": "propagated", "eta_seconds": eta_seconds}
