# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-02 04:50:00
# DESCRIPTION: Módulo de Logística com Diagnóstico Forense de Tenant e Permissões.

import math
import logging
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_
from typing import List, Any
from uuid import UUID
from datetime import datetime

from app.database import get_db, set_tenant
from app.models import Order, OrderStatus, Employee, Company, UserRole
from app.routers.auth import get_current_user
from app.websockets import manager

# Configuração de Log Forense
logger = logging.getLogger("ForensicLogistics")
logger.setLevel(logging.DEBUG)

router = APIRouter()

def calculate_eta_simple(curr_lat: float, curr_lng: float, dest_lat: float, dest_lng: float) -> int:
    """Enterprise ETA Model (Haversine)."""
    R = 6371000.0
    phi1, phi2 = math.radians(curr_lat), math.radians(dest_lat)
    dphi = math.radians(dest_lat - curr_lat)
    dlambda = math.radians(dest_lng - curr_lng)
    a = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return int((R * c / 5.5) * 1.25) if R * c > 0 else 60

def require_logistics_access(current_user: Any = Depends(get_current_user)):
    """
    🛡️ GUARDIÃO DE ACESSO (L6)
    Valida se o usuário tem permissão para operar logística.
    """
    user_type = type(current_user).__name__
    user_id = getattr(current_user, "id", "UNKNOWN")
    
    logger.info(f"🔍 [PERM_CHECK] User: {user_id} | Type: {user_type}")

    if user_type == "Company" or isinstance(current_user, Company):
        return current_user
    
    if user_type == "Employee" or isinstance(current_user, Employee):
        raw_role = getattr(current_user, "role", "NONE")
        role_str = str(raw_role.value if hasattr(raw_role, 'value') else raw_role).lower().strip()
        allowed = ["owner", "admin", "manager", "driver"]
        if role_str in allowed:
            return current_user

    logger.warning(f"❌ [PERM_FAIL] Acesso negado para {user_id} ({user_type})")
    raise HTTPException(status_code=403, detail="Acesso negado ao módulo de logística.")

@router.get("/orders", response_model=None)
def get_delivery_orders(
    db: Session = Depends(get_db), 
    current_user: Any = Depends(require_logistics_access)
):
    """
    🛡️ FILTRO SOBERANO: Retorna apenas pedidos PRONTOS e SEM MOTORISTA.
    """
    # Resolve Company ID baseando-se no tipo de objeto retornado pelo Auth
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    
    logger.info(f"🔭 [GET_ORDERS] Tenant: {company_id}")
    set_tenant(db, str(company_id))
    
    # 🛡️ HARDENING: Filtro triplo: Status Ready + Tipo Delivery + Driver ID Nulo
    orders = db.query(Order).filter(
        and_(
            Order.company_id == company_id,
            Order.status == "ready",
            Order.order_type == "delivery",
            Order.driver_id == None
        )
    ).order_by(Order.created_at.desc()).all()
    
    logger.info(f"📊 [GET_ORDERS] Disponíveis: {len(orders)} para CID {company_id}")
    return orders

@router.patch("/orders/{order_id}/dispatch", status_code=200)
async def dispatch_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_logistics_access)
):
    """Vincula o motorista ao pedido e inicia a rota."""
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    driver_id = current_user.id if not hasattr(current_user, 'owner_email') else None
    
    set_tenant(db, str(company_id))
    
    # Lock Pessimista para evitar race conditions no aceite
    order = db.query(Order).with_for_update().filter(Order.id == order_id, Order.company_id == company_id).first()
    
    if not order: 
        logger.error(f"❌ [DISPATCH] Pedido {order_id} não encontrado para CID {company_id}")
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if order.driver_id:
        raise HTTPException(status_code=409, detail="Este pedido já foi aceito por outro motorista.")

    order.status = "delivering"
    order.driver_id = driver_id
    db.commit()
    
    slug = db.query(Company.slug).filter(Company.id == company_id).scalar()
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": "delivering"}, slug)
    
    return {"message": "Rota iniciada"}

@router.patch("/orders/{order_id}/complete", status_code=200)
async def complete_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_logistics_access)
):
    """Finaliza a entrega do pedido."""
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    set_tenant(db, str(company_id))
    
    order = db.query(Order).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: 
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    order.status = "delivered"
    order.finished_at = datetime.now()
    db.commit()
    
    slug = db.query(Company.slug).filter(Company.id == company_id).scalar()
    await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": "delivered"}, slug)
    
    return {"message": "Entrega finalizada"}

@router.post("/orders/{order_id}/location", status_code=200)
async def update_order_location(
    order_id: UUID,
    lat: float = Body(..., embed=True),
    lng: float = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_logistics_access)
):
    """Propaga a localização do entregador via WebSocket."""
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    set_tenant(db, str(company_id))
    
    order = db.query(Order).options(selectinload(Order.company)).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order: 
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Destino padrão (Coordenadas da Loja - Exemplo Pompeu)
    eta = calculate_eta_simple(lat, lng, -19.22815, -44.94195)
    
    await manager.broadcast({
        "type": "DELIVERY_LOCATION",
        "order_id": str(order.id),
        "payload": {"lat": lat, "lng": lng, "eta_seconds": eta}
    }, order.company.slug)
    
    return {"status": "propagated", "eta_seconds": eta}