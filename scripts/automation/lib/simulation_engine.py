# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:45:00
import time
import requests
import random
from enum import Enum
from typing import Dict, Any, Optional, List

class SimState(Enum):
    IDLE = "idle"
    CREATED = "pending"
    PAID = "paid"
    PREPARING = "preparing"
    READY = "ready"
    DISPATCHED = "delivering"
    DELIVERED = "delivered"
    FAILED = "failed"

class StateMachine:
    """FSM Executável L8: Governa as transições permitidas no domínio."""
    _rules = {
        SimState.IDLE: [SimState.CREATED],
        SimState.CREATED: [SimState.PAID, SimState.FAILED],
        SimState.PAID: [SimState.PREPARING, SimState.FAILED],
        SimState.PREPARING: [SimState.READY, SimState.FAILED],
        SimState.READY: [SimState.DISPATCHED, SimState.FAILED],
        SimState.DISPATCHED: [SimState.DELIVERED, SimState.FAILED],
    }

    def __init__(self):
        self.current = SimState.IDLE

    def transition_to(self, next_state: SimState):
        if next_state not in self._rules.get(self.current, []):
            raise ValueError(f"🚫 Transição Inválida: {self.current.name} -> {next_state.name}")
        self.current = next_state
        return self.current

class ContractValidator:
    """Validador de Contratos de API v1.2.0."""
    @staticmethod
    def validate_order(data: Dict[str, Any]):
        required = ["id", "status", "total_amount", "customer_name"]
        for field in required:
            if field not in data:
                raise AssertionError(f"❌ Quebra de Contrato: Campo '{field}' ausente no payload do pedido.")
        return True

class SimulationTransaction:
    """Transaction Scope L8: Garante cleanup atômico do cenário de teste."""
    def __init__(self, api_url: str, slug: str, token: str):
        self.api_url = api_url
        self.slug = slug
        self.token = token
        self.order_id = None

    def __enter__(self):
        return self

    def set_order(self, order_id: str):
        self.order_id = order_id

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self.order_id:
            print(f"\n⛑️  CLEANUP: Abortando pedido {self.order_id} devido a falha no script.")
            headers = {"Authorization": f"Bearer {self.token}"}
            requests.patch(f"{self.api_url}/admin/orders/{self.order_id}", 
                          headers=headers, json={"status": "canceled"})
        return False # Propaga a exceção

class MetricsCollector:
    """Observabilidade Ativa L8: Streaming de eventos e latências."""
    def __init__(self, build_id: str):
        self.start_time = time.time()
        self.build_id = build_id
        self.events = []

    def record_transition(self, from_state: SimState, to_state: SimState, latency_ms: float):
        event = {
            "event": "STATE_TRANSITION",
            "from": from_state.value,
            "to": to_state.value,
            "latency_ms": round(latency_ms, 2),
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        print(f"📡 [OBS] {event['from']} -> {event['to']} | {event['latency_ms']}ms")

    def get_final_manifest(self, verdict: str) -> Dict[str, Any]:
        return {
            "spec": "L8_SIMULATION_SPEC@1.0",
            "build": self.build_id,
            "verdict": verdict,
            "total_duration_sec": round(time.time() - self.start_time, 2),
            "transitions": self.events
        }

from datetime import datetime # Necessário para o MetricsCollector

