"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 4.5.0 (Platinum Master Edition)
 * OBJETIVO: Router Soberano para Operações Móveis, Telemetria e Roteamento Proxy.
 * Comportamento esperado: 
 *  1. Gerencia ciclo de vida do motorista (Turnos e Jornadas).
 *  2. Atua como Proxy Soberano para Google Maps para ocultar chaves de API e resolver CORS.
 *  3. Orquestra transições de estado da FSM com isolamento RLS garantido.
 *  4. Ingestão massiva de telemetria em lote para economia de rádio/bateria.
 */
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Body, Query, status
from sqlalchemy.orm import Session
from typing import Union, Optional, Any
from datetime import datetime

from app.database import get_db, set_tenant
from app.routers.auth import get_current_user
from app.models import Company, Employee
from app.models.logistics import JourneyStatus
from app.schemas.logistics import (
    DriverAuth, 
    ShiftEndRequest, 
    TelemetryBatch, 
    DriverStateResponse,
    JourneyResponse,
    JourneyUpdate
)
from app.services.logistics_service import LogisticsService
from app.services.logistics_orchestrator import LogisticsOrchestrator
from app.services.google_maps_service import GoogleMapsService

logger = logging.getLogger("LogisticsMobile")
router = APIRouter()

def get_logistics_actor(current_user: Union[Company, Employee] = Depends(get_current_user)) -> Union[Company, Employee]:
    if isinstance(current_user, Company):
        return current_user
    if isinstance(current_user, Employee):
        role = str(current_user.role).lower().strip()
        if role in ["driver", "owner", "manager", "admin"]:
            return current_user
    logger.warning(f"SECURITY_ALERT: Unauthorized logistics access attempt by {getattr(current_user, 'email', 'anonymous')}")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCESS_DENIED_LOGISTICS_DOMAIN")

def _resolve_driver_id(db: Session, actor: Union[Company, Employee]) -> int:
    if isinstance(actor, Employee):
        return int(actor.id)
    owner_emp = db.query(Employee).filter(Employee.email == actor.owner_email).first()
    if not owner_emp:
        raise HTTPException(status_code=404, detail="OPERATIONAL_IDENTITY_NOT_FOUND")
    return int(owner_emp.id)

@router.get("/route")
async def get_sovereign_route(
    origin: str = Query(..., description="lat,lng"),
    dest: str = Query(..., description="lat,lng"),
    actor: Union[Company, Employee] = Depends(get_logistics_actor)
):
    try:
        o_lat, o_lng = map(float, origin.split(","))
        d_lat, d_lng = map(float, dest.split(","))
        route = await GoogleMapsService.get_route(o_lat, o_lng, d_lat, d_lng)
        if not route:
            raise HTTPException(status_code=404, detail="ROUTING_ENGINE_EMPTY_RESPONSE")
        return route
    except Exception as e:
        logger.error(f"ROUTING_CRITICAL_FAIL: {str(e)}")
        raise HTTPException(status_code=500, detail="INTERNAL_ROUTING_ERROR")

@router.post("/shift/start", response_model=DriverStateResponse)
def start_shift(
    data: DriverAuth,
    db: Session = Depends(get_db),
    actor: Union[Company, Employee] = Depends(get_logistics_actor)
):
    company_id = actor.id if isinstance(actor, Company) else actor.company_id
    set_tenant(db, str(company_id))
    driver_id = _resolve_driver_id(db, actor)
    shift = LogisticsService.start_shift(db, driver_id, data.vehicle_id, data.battery_level)
    logger.info(f"SHIFT_STARTED: Driver {driver_id} on {data.vehicle_id}")
    return {
        "shift_id": shift.id,
        "status": "IDLE",
        "today_metrics": {"earnings": float(shift.total_earnings or 0.0), "km": 0.0, "rides": 0}
    }

@router.post("/shift/end")
def end_shift(
    data: ShiftEndRequest,
    db: Session = Depends(get_db),
    actor: Union[Company, Employee] = Depends(get_logistics_actor)
):
    company_id = actor.id if isinstance(actor, Company) else actor.company_id
    set_tenant(db, str(company_id))
    driver_id = _resolve_driver_id(db, actor)
    LogisticsService.end_shift(db, driver_id, data.final_battery, data.estimated_km)
    logger.info(f"SHIFT_ENDED: Driver {driver_id}")
    return {"status": "OFFLINE"}

@router.post("/journey/{order_id}/accept", response_model=JourneyResponse)
def accept_journey(
    order_id: str,
    db: Session = Depends(get_db),
    actor: Union[Company, Employee] = Depends(get_logistics_actor)
):
    company_id = actor.id if isinstance(actor, Company) else actor.company_id
    set_tenant(db, str(company_id))
    driver_id = _resolve_driver_id(db, actor)
    journey = LogisticsService.accept_journey(db, driver_id, order_id)
    return {
        "id": journey.id, 
        "order_id": journey.order_id, 
        "status": journey.status, 
        "created_at": journey.accepted_at
    }

@router.patch("/journey/{journey_id}/status")
def update_journey_status(
    journey_id: str,
    payload: JourneyUpdate,
    db: Session = Depends(get_db),
    actor: Union[Company, Employee] = Depends(get_logistics_actor)
):
    company_id = actor.id if isinstance(actor, Company) else actor.company_id
    set_tenant(db, str(company_id))
    try:
        target_status = payload.status.upper()
        update_data = payload.model_dump(exclude_unset=True)
        journey = LogisticsOrchestrator.update_journey_state(db, journey_id, target_status, update_data)
        return {"status": "success", "new_state": journey.status}
    except Exception as e:
        logger.error(f"FSM_TRANSITION_ERROR: {journey_id} -> {payload.status} | {str(e)}")
        raise HTTPException(status_code=500, detail="FSM_TRANSITION_FAILED")

@router.post("/telemetry")
def ingest_telemetry(
    batch: TelemetryBatch,
    db: Session = Depends(get_db),
    actor: Union[Company, Employee] = Depends(get_logistics_actor)
):
    company_id = actor.id if isinstance(actor, Company) else actor.company_id
    set_tenant(db, str(company_id))
    driver_id = _resolve_driver_id(db, actor)
    return LogisticsService.process_telemetry(db, driver_id, batch)

@router.patch("/vehicle/active")
def update_vehicle(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    actor: Union[Company, Employee] = Depends(get_logistics_actor)
):
    company_id = actor.id if isinstance(actor, Company) else actor.company_id
    set_tenant(db, str(company_id))
    driver_id = _resolve_driver_id(db, actor)
    vehicle_id = payload.get("vehicle_id")
    if not vehicle_id:
        raise HTTPException(status_code=400, detail="VEHICLE_ID_REQUIRED")
    LogisticsService.update_active_vehicle(db, driver_id, str(vehicle_id))
    return {"status": "success", "vehicle_id": vehicle_id}