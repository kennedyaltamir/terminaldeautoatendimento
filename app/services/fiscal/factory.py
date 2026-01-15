# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-14 22:30:00
import os
import logging
from app.services.fiscal.interfaces import FiscalProvider
from app.services.fiscal.providers.mock import MockProvider
from app.services.fiscal.providers.focus_nfe import FocusNFeProvider

logger = logging.getLogger("FiscalFactory")

def get_fiscal_provider() -> FiscalProvider:
    """
    Fábrica que retorna a implementação correta do provedor fiscal.
    Implementa salvaguarda contra ativação acidental de produção.
    """
    provider_name = os.getenv("FISCAL_PROVIDER", "mock").lower()
    fiscal_env = os.getenv("FISCAL_ENV", "sandbox").lower()

    # SALVAGUARDA: Proteção contra Go-Live acidental
    if fiscal_env == "production":
        confirmed = os.getenv("FISCAL_PRODUCTION_CONFIRMED", "false").lower() == "true"
        if not confirmed:
            logger.critical("🔥 BLOQUEIO DE SEGURANÇA: FISCAL_ENV=production detectado, mas FISCAL_PRODUCTION_CONFIRMED não é 'true'.")
            # Fallback forçado para Mock em caso de erro de config para não crashar o boot, 
            # mas emitir erro grave no log.
            return MockProvider()

    if provider_name == "focus":
        logger.info(f"🧾 Provedor Fiscal Ativo: Focus NFe ({fiscal_env})")
        return FocusNFeProvider()
    
    return MockProvider()

