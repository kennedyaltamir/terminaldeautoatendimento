"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 3.3.0 (Diamond Hardened Master)
 * DNA_ID: MF-SERV-LOG-V3-3
 * OBJETIVO: Serviço de Logística com Tipagem Estrita e Resiliência Temporal.
 * Comportamento esperado: 
 *  1. Gerencia o ciclo de vida de turnos (Shifts) com auto-healing de sessões órfãs.
 *  2. Orquestra o aceite de jornadas (Journeys) com lock pessimista para evitar race conditions.
 *  3. Processa telemetria em lote com normalização de fuso horário (Aware Datetime).
 *  4. Garante integridade de tipos para conformidade total com Pyright/MyPy.
 */
"""

import logging
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timezone
from fastapi import HTTPException
from typing import Any, List, cast
from app.models.logistics import DriverShift, LogisticsJourney, JourneyStatus, DriverTelemetry
from app.models.orders import Order, OrderStatus
from app.models.auth import Employee
from app.schemas.logistics import TelemetryBatch

logger = logging.getLogger("LogisticsService")

class LogisticsService:
    """
    Serviço Soberano de Logística.
    Responsável pela lógica de negócio de movimentação, turnos e telemetria.
    """

    @staticmethod
    def start_shift(db: Session, driver_id: int, vehicle_id: str, battery: float) -> DriverShift:
        """
        Inicia o turno do motorista.
        Implementa rito de auto-healing: encerra turnos anteriores que ficaram abertos por falha de rede.
        """
        now_utc = datetime.now(timezone.utc)
        
        # 🛡️ TÁTICA: Localiza e encerra turnos "zumbis"
        open_shifts = db.query(DriverShift).filter(
            DriverShift.driver_id == driver_id,
            DriverShift.ended_at.is_(None) # 🛡️ FIX: E711
        ).all()
        
        for shift in open_shifts:
            shift.ended_at = cast(Any, now_utc)
            logger.info(f"Auto-closing stale shift {shift.id} for driver {driver_id}")

        # Validação de Identidade
        driver = db.query(Employee).filter(Employee.id == driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="Motorista não encontrado no Kernel.")

        # Criação do Turno
        new_shift = DriverShift(
            driver_id=driver_id,
            company_id=driver.company_id,
            vehicle_id=vehicle_id,
            battery_start_level=battery,
            started_at=now_utc
        )
        
        db.add(new_shift)
        db.commit()
        db.refresh(new_shift)
        return new_shift

    @staticmethod
    def end_shift(db: Session, driver_id: int, final_battery: float, estimated_km: float) -> None:
        """
        Encerra o turno ativo.
        Calcula a duração total em minutos garantindo compatibilidade de fuso horário.
        """
        shift = db.query(DriverShift).filter(
            DriverShift.driver_id == driver_id,
            DriverShift.ended_at.is_(None) # 🛡️ FIX: E711
        ).order_by(desc(DriverShift.started_at)).first()
        
        if not shift:
            logger.warning(f"Tentativa de encerrar turno inexistente para driver {driver_id}")
            return

        now_utc = datetime.now(timezone.utc)
        shift.ended_at = cast(Any, now_utc)
        shift.battery_end_level = cast(Any, final_battery)
        shift.total_km_driven = cast(Any, estimated_km)

        # Cálculo de SLA/Duração
        if bool(shift.started_at):
            start_time = cast(datetime, shift.started_at)
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            
            delta = now_utc - start_time
            shift.total_online_minutes = cast(Any, int(delta.total_seconds() / 60))

        db.commit()
        logger.info(f"Shift {shift.id} finalizado. Duração: {shift.total_online_minutes} min.")

    @staticmethod
    def accept_journey(db: Session, driver_id: int, order_id: str) -> LogisticsJourney:
        """
        Rito de Aceite de Missão.
        Utiliza Lock Pessimista (FOR UPDATE) para garantir que dois motoristas não aceitem o mesmo pedido.
        """
        # 1. Valida Turno Ativo
        shift = db.query(DriverShift).filter(
            DriverShift.driver_id == driver_id,
            DriverShift.ended_at.is_(None) # 🛡️ FIX: E711
        ).first()

        if not shift:
            raise HTTPException(status_code=403, detail="Acesso negado: Turno inativo ou não iniciado.")

        # 2. Adquire Lock no Pedido
        order = db.query(Order).with_for_update().filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido não encontrado para aceite.")
        
        # 3. Valida Disponibilidade (Anti-Race Condition)
        if bool(order.driver_id) and int(cast(Any, order.driver_id)) != driver_id:
            raise HTTPException(status_code=409, detail="Esta missão já foi capturada por outro operador.")

        # 4. Criação da Jornada
        journey = LogisticsJourney(
            shift_id=shift.id,
            order_id=order.id,
            driver_id=driver_id,
            company_id=order.company_id,
            status=JourneyStatus.ASSIGNED.value,
            accepted_at=datetime.now(timezone.utc)
        )

        # 5. Atualização Atômica do Pedido
        order.driver_id = cast(Any, driver_id)
        order.status = cast(Any, OrderStatus.DELIVERING.value)
        
        db.add(journey)
        db.commit()
        db.refresh(journey)
        
        logger.info(f"Jornada {journey.id} iniciada para o pedido {order_id}")
        return journey

    @staticmethod
    def process_telemetry(db: Session, driver_id: int, batch: TelemetryBatch) -> dict:
        """
        Ingestão de telemetria em lote.
        Vincula pontos à jornada ativa se houver, caso contrário registra como telemetria de prontidão.
        """
        telemetry_objects: List[DriverTelemetry] = []
        
        # Busca jornada ativa para vínculo
        active_journey = db.query(LogisticsJourney).filter(
            LogisticsJourney.driver_id == driver_id,
            LogisticsJourney.completed_at == None
        ).first()
        
        journey_id = active_journey.id if active_journey else None

        for point in batch.points:
            ts = point.timestamp
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
                
            telemetry_objects.append(DriverTelemetry(
                driver_id=driver_id,
                journey_id=journey_id,
                lat=point.lat,
                lng=point.lng,
                speed=point.speed,
                heading=point.heading,
                accuracy=point.accuracy,
                battery_level=batch.battery_level,
                timestamp=ts
            ))

        if telemetry_objects:
            db.bulk_save_objects(telemetry_objects)
            db.commit()
            
        return {"status": "PROCESSED", "count": len(telemetry_objects)}

    @staticmethod
    def update_active_vehicle(db: Session, driver_id: int, vehicle_id: str) -> None:
        """
        Atualiza o identificador do veículo para o turno atual.
        """
        shift = db.query(DriverShift).filter(
            DriverShift.driver_id == driver_id,
            DriverShift.ended_at == None
        ).first()
        
        if shift:
            shift.vehicle_id = cast(Any, vehicle_id)
            db.commit()
            logger.info(f"Veículo do turno {shift.id} atualizado para {vehicle_id}")