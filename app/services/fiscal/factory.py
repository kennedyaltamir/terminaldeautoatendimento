import os
from app.services.fiscal.interfaces import FiscalProvider
from app.services.fiscal.providers.mock import MockProvider
from app.services.fiscal.providers.focus_nfe import FocusNFeProvider

def get_fiscal_provider() -> FiscalProvider:
    """
    Fábrica que retorna a implementação correta do provedor fiscal
    baseada nas variáveis de ambiente.
    """
    provider_name = os.getenv("FISCAL_PROVIDER", "mock").lower()
    
    if provider_name == "focus":
        return FocusNFeProvider()
    
    # Default para Mock (Segurança para Dev)
    return MockProvider()