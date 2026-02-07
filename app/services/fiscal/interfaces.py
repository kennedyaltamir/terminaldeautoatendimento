# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models import Order, Company

class FiscalProvider(ABC):
    """
    Interface abstrata para provedores de emissão fiscal.
    Garante que o sistema possa trocar de fornecedor (eNotas, Focus, Nuvem)
    sem alterar a lógica de negócio principal.
    """

    @abstractmethod
    async def emit_invoice(self, order: Order, company: Company) -> Dict[str, Any]:
        """
        Solicita a emissão de uma NFC-e.
        
        Retorno esperado:
        {
            "status": "processing" | "emitted" | "error",
            "provider_reference": str (ID do pedido no sistema deles),
            "message": str,
            "nfe_url": str (Opcional, se síncrono)
        }
        """
        pass

    @abstractmethod
    async def cancel_invoice(self, order: Order, company: Company, reason: str) -> Dict[str, Any]:
        """
        Solicita o cancelamento de uma nota.
        """
        pass