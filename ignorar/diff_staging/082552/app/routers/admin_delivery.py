# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 15:30:00
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import Order, OrderStatus, Employee, UserRole
from app.routers.auth import get_current_user
from app.websockets import manager

router = APIRouter()

@router.get("/orders", response_model=List[any])
def get_delivery_orders(db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    # Retorna apenas pedidos prontos ou em entrega para o contexto logístico
    return db.query(Order).filter(
        Order.company_id == company_id,
        Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
    ).order_by(Order.created_at.desc()).all()

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Inicia a entrega com Lock Transacional (Regra L6):
    1. O entregador deve estar livre (sem outro delivering).
    2. O pedido deve estar pronto (ready).
    """
    company_id = getattr(current_user, "company_id", getattr(current_user, "id", None))
    driver_id = getattr(current_user, "id", None) if hasattr(current_user, "role") and current_user.role == "driver" else None

    # 1. Verifica se o entregador já tem algo em andamento
    if driver_id:
        active_job = db.query(Order).filter(Order.driver_id == driver_id, Order.status == OrderStatus.DELIVERING).first()
        if active_job:
            raise HTTPException(400, "Você já possui uma entrega em andamento.")

    # 2. Busca e valida pedido
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: raise HTTPException(404, "Pedido não encontrado")
    if order.status != OrderStatus.READY:
        raise HTTPException(400, f"Pedido não pode ser coletado (Status: {order.status})")

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
    current_user: any = Depends(get_current_user)
):
    """Propaga a localização GPS padrão V1 (L6 Compliance)."""
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
