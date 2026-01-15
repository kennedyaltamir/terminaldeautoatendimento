# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 12:45:00
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus, Company, OrderType, OrderItem
from app.routers.auth import get_current_user
from app.schemas import OrderResponse, DispatchOrderRequest
from app.websockets import manager

router = APIRouter()

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")
    order.status = OrderStatus.DELIVERING
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
    current_user: any = Depends(get_current_user)
):
    """Propaga a localização GPS padrão V1 (L6 Compliance)."""
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")

    # Payload padronizado conforme v1 da especificação de tracking geográfico
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
