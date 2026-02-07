# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-05 03:42:00
import time
import logging
import os
from typing import Optional, Dict, Any
from app.core.cache import CacheService
from app.core import security

logger = logging.getLogger("CircuitBreaker")

class CircuitBreaker:
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 30
    
    @classmethod
    async def check_health(cls, request: any):
        # Verifica estado no Redis
        state = CacheService.get("cb:state") or "CLOSED"
        if state == "OPEN":
            last_fail = CacheService.get("cb:open_at")
            if last_fail and (time.time() - float(last_fail) > cls.RECOVERY_TIMEOUT):
                CacheService.set("cb:state", "HALF_OPEN", 10)
                return
            raise Exception("CIRCUIT_BREAKER_OPEN")

    @classmethod
    def record_error(cls):
        """🛡️ FIX: Método de registro de erro restaurado."""
        try:
            count = CacheService.incr("cb:error_count")
            if count >= cls.FAILURE_THRESHOLD:
                CacheService.set("cb:state", "OPEN", 60)
                CacheService.set("cb:open_at", time.time(), 60)
                logger.critical(f"🚨 CIRCUIT BREAKER ABERTO: {count} falhas.")
        except: pass

    @classmethod
    def record_success(cls):
        """🛡️ FIX: Método de limpeza restaurado."""
        try:
            CacheService.delete("cb:error_count")
            CacheService.set("cb:state", "CLOSED")
        except: pass