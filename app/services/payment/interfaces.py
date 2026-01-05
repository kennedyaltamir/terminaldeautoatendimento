from abc import ABC, abstractmethod
from typing import Dict, Any
from decimal import Decimal
from app.models import Order, Company

class PaymentProviderInterface(ABC):
    """
    Contrato obrigatório para qualquer gateway de pagamento integrado ao MesaFlow.
    """

    @abstractmethod
    async def create_pix_payment(self, order: Order, company: Company, split_rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera um pagamento Pix.
        Deve retornar: { "id": str, "qr_code": str, "qr_code_base64": str, "status": str }
        """
        pass

    @abstractmethod
    async def get_auth_url(self, state: str) -> str:
        """Retorna a URL para o usuário conectar sua conta (OAuth)"""
        pass

    @abstractmethod
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Troca o código de autorização por credenciais definitivas"""
        pass