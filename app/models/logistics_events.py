# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-28 20:15:00
"""
MesaFlow Logistics Audit Events
Standardized Enum for Driver/System interactions to ensure forensic consistency.
"""
from enum import Enum

class DriverAuditEvent(str, Enum):
    # --- OPERATIONAL FLOW ---
    SHIFT_START = "SHIFT_START"
    SHIFT_END = "SHIFT_END"
    ROUTE_ACCEPTED = "ROUTE_ACCEPTED"
    PICKUP_CONFIRMED = "PICKUP_CONFIRMED"
    DELIVERY_COMPLETED = "DELIVERY_COMPLETED"
    
    # --- EXCEPTIONS & INCIDENTS ---
    INCIDENT_REPORTED = "INCIDENT_REPORTED"
    WAIT_TIMER_STARTED = "WAIT_TIMER_STARTED"
    WAIT_TIMER_EXPIRED = "WAIT_TIMER_EXPIRED"
    RETURN_TO_BASE = "RETURN_TO_BASE"
    
    # --- SYSTEMIC EVENTS ---
    TELEMETRY_LOST = "TELEMETRY_LOST"
    TELEMETRY_RECOVERED = "TELEMETRY_RECOVERED"
    OFFLINE_SYNC_BATCH = "OFFLINE_SYNC_BATCH"
    PRESSURE_MODE_AUTO_ON = "PRESSURE_MODE_AUTO_ON"
    PRESSURE_MODE_AUTO_OFF = "PRESSURE_MODE_AUTO_OFF"
    
    # --- SECURITY ---
    GEOFENCE_MISMATCH_OVERRIDE = "GEOFENCE_MISMATCH_OVERRIDE"
    POD_FAILURE = "POD_FAILURE"

class IncidentSeverity(str, Enum):
    LOW = "LOW"         # Informational (e.g., slight delay)
    MEDIUM = "MEDIUM"   # Operational (e.g., wait timer)
    HIGH = "HIGH"       # Financial Risk (e.g., return to base)
    CRITICAL = "CRITICAL" # Safety/Legal (e.g., accident, aggression)

