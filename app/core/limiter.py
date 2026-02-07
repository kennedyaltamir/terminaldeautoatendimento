# DOMAIN: BACKEND / INFRA
# LAST_MODIFIED: 2026-01-27 23:30:00
# DESCRIPTION: Rate Limiter - Neutralização Total para Localhost e Automação.
import os
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger("Limiter")
IS_DEV = os.getenv("ENVIRONMENT", "development") == "development"

def custom_key_func(request):
    # 🛡️ BYPASS ABSOLUTO: Se for localhost ou ambiente de dev, retorna uma chave fixa
    client_ip = get_remote_address(request)
    if IS_DEV or client_ip in ["127.0.0.1", "localhost", "::1"]:
        return "internal_automation_bypass"
    return client_ip

# Configuração: Em DEV, o limite é virtualmente infinito (1 milhão de reqs/min)
limiter = Limiter(
    key_func=custom_key_func,
    default_limits=["1000000/minute"] if IS_DEV else ["1000/day", "100/hour"]
)
