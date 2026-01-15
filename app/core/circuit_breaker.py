
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-12 21:25:00
import time
import logging
import random
from fastapi import HTTPException
from app.core.cache import CacheService

logger = logging.getLogger("CircuitBreaker")

class CircuitBreaker:
    THRESHOLD_ERRORS = 20
    THRESHOLD_SUCCESS = 5
    WINDOW_SECONDS = 60
    RECOVERY_TIMEOUT = 30
    
    @classmethod
    async def get_state(cls):
        if not CacheService._enabled: return "CLOSED"
        return CacheService.get("cb:state") or "CLOSED"

    @classmethod
    async def check_health(cls):
        if not CacheService._enabled: return
        
        state = await cls.get_state()
        if state == "OPEN":
            open_time = float(CacheService.get("cb:open_at") or 0)
            if time.time() - open_time > cls.RECOVERY_TIMEOUT:
                cls._set_state("HALF_OPEN")
                return
            raise HTTPException(status_code=503, detail="Sistema em modo de proteção (SLA_BREACH).")
        
        if state == "HALF_OPEN":
            if random.random() > 0.2:
                raise HTTPException(status_code=503, detail="Recuperação em curso.")
        return

    @classmethod
    def record_success(cls):
        if not CacheService._enabled: return
        state = CacheService.get("cb:state")
        if state == "HALF_OPEN":
            client = cls._get_redis()
            if client:
                success_count = client.incr("cb:success_count")
                if success_count >= cls.THRESHOLD_SUCCESS:
                    cls._set_state("CLOSED")

    @classmethod
    def record_error(cls):
        if not CacheService._enabled: return
        state = CacheService.get("cb:state") or "CLOSED"
        client = cls._get_redis()
        if not client: return

        if state == "CLOSED":
            error_count = client.incr("cb:error_count")
            client.expire("cb:error_count", cls.WINDOW_SECONDS)
            if error_count >= cls.THRESHOLD_ERRORS:
                cls._set_state("OPEN")
                client.set("cb:open_at", str(time.time()))
        elif state == "HALF_OPEN":
            cls._set_state("OPEN")
            client.set("cb:open_at", str(time.time()))

    @classmethod
    def _set_state(cls, state):
        client = cls._get_redis()
        if client:
            client.set("cb:state", state)
            if state != "HALF_OPEN": client.delete("cb:success_count")
            if state == "CLOSED": client.delete("cb:error_count")

    @classmethod
    def _get_redis(cls):
        return CacheService._client if CacheService._enabled else None

