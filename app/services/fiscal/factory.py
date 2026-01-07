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
    fiscal_env = os.getenv("FISCAL_ENV", "mock").lower()

    # SALVAGUARDA: Proteção contra Go-Live acidental
    if fiscal_env == "production":
        confirmed = os.getenv("FISCAL_PRODUCTION_CONFIRMED", "false").lower() == "true"
        if not confirmed:
            logger.critical("🔥 BLOQUEIO DE SEGURANÇA: FISCAL_ENV=production detectado, mas FISCAL_PRODUCTION_CONFIRMED não é 'true'.")
            raise RuntimeError("Configuração fiscal de produção incompleta. Ativação negada.")

    # Se o ambiente for explicitamente 'mock', ignoramos o provedor e usamos o simulador
    if fiscal_env == "mock" or provider_name == "mock":
        return MockProvider()

    if provider_name == "focus":
        return FocusNFeProvider()

    return MockProvider()
