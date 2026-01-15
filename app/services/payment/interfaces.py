
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 01:00:00
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.models.company import Company
class PaymentProviderInterface(ABC):
    @abstractmethod
    async def create_pix_payment(self, order: any, company: Company, split_rules: Dict[str, Any]) -> Dict[str, Any]:
        pass
    @abstractmethod
    async def get_auth_url(self, state: str) -> str:
        pass
    @abstractmethod
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        pass
    @abstractmethod
    async def get_transaction_history(self, company: Company, days: int = 1) -> List[Dict[str, Any]]:
        """
        Busca o histórico de transações no provedor para conciliação.
        Deve retornar lista de: {"external_id": str, "amount_cents": int, "status": str}
        """
        pass
