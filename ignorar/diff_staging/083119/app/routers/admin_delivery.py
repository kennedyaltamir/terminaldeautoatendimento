# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 16:30:00
import math
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, selectinload
from typing import List, Any, Optional
from uuid import UUID
from datetime import datetime
from app.database import get_db
from app.models import Order, OrderStatus
from app.routers.auth import get_current_user
from app.websockets import manager

router = APIRouter()

def calculate_eta_simple(curr_lat: float, curr_lng: float, dest_lat: float, dest_lng: float) -> int:
    """
    Cálculo de ETA Enterprise-Grade (Haversine + Velocidade Média).
    Evita chamadas excessivas a APIs de roteamento externas.
    """
    # Raio da Terra em metros
    R = 6371000
    phi1, phi2 = math.radians(curr_lat), math.radians(dest_lat)
    dphi = math.radians(dest_lat - curr_lat)
    dlamb = math.radians(dest_lng - curr_lng)
    
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlamb/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance_meters = R * c

    # Velocidade média urbana estimada para moto: 20km/h => 5.5 m/s
    # Inclui buffer de 25% para semáforos e trânsito
    avg_speed_mps = 5.5
    eta_seconds = int((distance_meters / avg_speed_mps) * 1.25)
    
    return max(60, eta_seconds) # Mínimo de 1 minuto

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
    """
    Inicia a entrega com LOCK TRANSACIONAL (Strict L6).
    Garante que o estado do banco seja a única fonte de verdade concorrente.
    """
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    driver_id = getattr(current_user, "id", None)
    
    # 🛡️ LOCK 1: Garante que o driver só tenha 1 pedido em delivering por vez
    active_job = db.query(Order).with_for_update().filter(
        Order.driver_id == driver_id, 
        Order.status == OrderStatus.DELIVERING
    ).first()
    
    if active_job:
        raise HTTPException(400, "Você já possui uma entrega em andamento.")

    # 🛡️ LOCK 2: Reserva o pedido para este driver, impedindo double-dispatch
    order = db.query(Order).with_for_update().options(selectinload(Order.company)).filter(
        Order.id == order_id, 
        Order.company_id == company_id
    ).first()
    
    if not order: raise HTTPException(404, "Pedido não encontrado")
    if order.status != OrderStatus.READY:
        raise HTTPException(400, "Pedido já coletado por outro entregador.")

    order.status = OrderStatus.DELIVERING
    order.driver_id = driver_id
    db.commit()
    
    # 📢 Evento v2: delivery.status
    await manager.broadcast({
        "type": "delivery.status", 
        "payload": {
            "order_id": str(order.id), 
            "status": "delivering"
        }
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
    """
    Atualiza localização com Validação de Ownership (Produção Ativa).
    Calcula ETA suavizado sem requisições externas.
    """
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    # 🛡️ SECURITY GUARD: Apenas o entregador do pedido pode atualizar o GPS
    if order.driver_id != current_user.id:
        raise HTTPException(403, "Acesso negado: você não é o entregador deste pedido.")
    
    if order.status != OrderStatus.DELIVERING:
        raise HTTPException(400, "Pedido não está mais em rota de entrega.")

    # Destino Mock Pompéu (Em produção: extraído de order.delivery_lat/lng)
    dest_lat, dest_lng = -19.22815, -44.94195
    eta_seconds = calculate_eta_simple(lat, lng, dest_lat, dest_lng)

    # 📢 Evento v2: delivery.location
    await manager.broadcast({
        "type": "delivery.location",
        "payload": {
            "order_id": str(order.id),
            "lat": lat,
            "lng": lng,
            "eta_seconds": eta_seconds
        },
        "v": 2
    }, order.company.slug)
    
    return {"status": "propagated", "eta_seconds": eta_seconds}
