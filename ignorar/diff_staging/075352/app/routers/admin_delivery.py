# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 14:15:00
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, selectinload
from typing import Optional
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus
from app.routers.auth import get_current_user
from app.websockets import manager

router = APIRouter()

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Inicia a rota de entrega. 
    Sincroniza o status 'delivering' via WS para mover o stepper do cliente.
    """
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")
    
    order.status = OrderStatus.DELIVERING
    db.commit()
    
    # 📢 NOTIFICAÇÃO CRÍTICA: Move o stepper do cliente para 'EM ROTA'
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
    current_user: any = Depends(get_current_user)
):
    """Propaga a localização GPS para o mapa em tempo real."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    await manager.broadcast({
        "type": "DELIVERY_LOCATION",
        "payload": {
            "order_id": str(order.id),
            "lat": lat,
            "lng": lng
        },
        "v": 1
    }, order.company.slug)
    
    return {"status": "location_broadcasted"}
