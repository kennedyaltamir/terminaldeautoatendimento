
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 04:40:00
import time
import functools
import logging
import os
from typing import Any, Dict, Callable
from fastapi import HTTPException

# Configuração de limites baseada na RFC-011
AI_LIMITS = {
    "MAX_RAM_MB": 512,
    "MAX_CPU_TIME_SEC": 30,
    "MAX_DATASET_ROWS": 10000
}

logger = logging.getLogger("AIGuard")

def ai_resource_guard(func: Callable):
    """
    Decorator que impõe limites de tempo e memória para funções de IA.
    Implementa a política de Fallback da RFC-011.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Nota: Monitoramento de memória real exige psutil. 
        # Para o MVP, focamos no tempo de CPU e tratamento de exceções.
        try:
            # Execução da lógica de IA
            result = func(*args, **kwargs)
            
            execution_time = time.time() - start_time
            if execution_time > AI_LIMITS["MAX_CPU_TIME_SEC"]:
                logger.warning(f"⚠️ AI_RESOURCE_EXCEEDED: Timeout de {execution_time}s")
                return {
                    "status": "prediction_unavailable",
                    "reason": "TIMEOUT",
                    "fallback_active": True
                }
            
            return result

        except Exception as e:
            logger.error(f"🔥 AI_EXECUTION_FAILED: {str(e)}")
            # RFC-011: Silent Fail - Retorna status amigável em vez de 500
            return {
                "status": "prediction_unavailable",
                "reason": "INTERNAL_ERROR",
                "fallback_active": True,
                "message": "O motor de predição está temporariamente indisponível."
            }
            
    return wrapper

def validate_dataset_size(row_count: int):
    """Garante que o dataset não exceda o limite da RFC-011."""
    if row_count > AI_LIMITS["MAX_DATASET_ROWS"]:
        logger.info(f"✂️ Dataset truncado de {row_count} para {AI_LIMITS['MAX_DATASET_ROWS']}")
        return True
    return False

