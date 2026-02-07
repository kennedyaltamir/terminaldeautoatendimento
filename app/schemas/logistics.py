# DOMAIN: BACKEND / SCHEMAS
# VERSION: 3.2.0 (Gold Master - Contract Aligned)
# LAST_MODIFIED: 2026-02-05 06:05:00
# DESCRIPTION: Schema Pydantic blindado para logística. Alinhado estritamente com o Frontend v4.4.0.

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# ==========================================
# 📥 INPUT SCHEMAS (REQUESTS)
# ==========================================

class DriverAuth(BaseModel):
    """
    Payload para início de turno.
    """
    vehicle_id: str = Field(..., description="Identificador do veículo (Placa ou ID interno)")
    battery_level: float = Field(..., ge=0.0, le=1.0, description="Nível de bateria do dispositivo (0.0 a 1.0)")
    
    model_config = ConfigDict(extra='ignore')

class ShiftEndRequest(BaseModel):
    """
    Payload para encerramento de turno.
    🛡️ CRITICAL: Nomes de campos alinhados com useDriverMachine.ts
    """
    final_battery: float = Field(..., description="Nível de bateria no encerramento (0.0 a 1.0)")
    estimated_km: float = Field(..., description="Total de KM rodados calculados pelo dispositivo")

    model_config = ConfigDict(extra='ignore')

class TelemetryPoint(BaseModel):
    """
    Ponto único de telemetria GPS.
    """
    lat: float
    lng: float
    speed: Optional[float] = 0.0
    heading: Optional[float] = 0.0
    accuracy: Optional[float] = 0.0
    timestamp: datetime
    
    # Campo opcional para debug de origem (Mobile vs Desktop)
    device_type: Optional[str] = None

    model_config = ConfigDict(extra='ignore')

class TelemetryBatch(BaseModel):
    """
    Lote de telemetria para ingestão eficiente.
    """
    points: List[TelemetryPoint]
    battery_level: float = 1.0

class PodSubmission(BaseModel):
    """
    Envio específico de Comprovante de Entrega (Proof of Delivery).
    """
    code: str = Field(..., min_length=4, max_length=10)
    lat: Optional[float] = None
    lng: Optional[float] = None

class IncidentReport(BaseModel):
    """
    Relatório de incidentes em rota.
    """
    reason: str
    description: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class JourneyUpdate(BaseModel):
    """
    Payload genérico para atualização de status da jornada via Orchestrator.
    """
    status: str
    pod_code: Optional[str] = None
    reason: Optional[str] = None
    tip_amount: Optional[float] = 0.0

# ==========================================
# 📤 OUTPUT SCHEMAS (RESPONSES)
# ==========================================

class DriverStateResponse(BaseModel):
    """
    Retorno do estado atual do motorista após login ou início de turno.
    """
    shift_id: Optional[UUID] = None
    status: str  # IDLE, EN_ROUTE, OFFLINE, etc.
    active_journey: Optional[Dict[str, Any]] = None
    today_metrics: Dict[str, Any]  # { earnings, km, rides }
    
    model_config = ConfigDict(from_attributes=True)

class JourneyResponse(BaseModel):
    """
    Detalhes da jornada para o frontend.
    """
    id: UUID
    order_id: UUID
    status: str
    
    customer_name: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    fee: Optional[float] = 0.0
    
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)