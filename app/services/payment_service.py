from sqlalchemy.orm import Session
from app.models import Order, Company, PaymentProvider
from app.services.payment.factory import PaymentFactory
import logging

logger = logging.getLogger("PaymentService")

class PaymentService:
    async def create_pix_payment(self, order: Order, company: Company):
        """
        Orquestrador que decide qual provedor usar baseado na configuração da empresa.
        """
        # 1. Verifica qual provedor a empresa usa
        provider_enum = company.payment_provider
        
        # Fallback para modo manual (sem integração)
        if provider_enum == PaymentProvider.NONE or not provider_enum:
            return self._generate_static_pix_mock(order, company)

        try:
            # 2. Instancia o provedor correto via Factory
            provider = PaymentFactory.get_provider(provider_enum)
            
            # 3. Define regras de negócio (Split)
            split_rules = {
                "fee_percentage": float(company.marketplace_fee_percentage or 0)
            }
            
            # 4. Executa
            return await provider.create_pix_payment(order, company, split_rules)
            
        except Exception as e:
            logger.error(f"Erro no pagamento ({provider_enum}): {e}")
            raise e

    def _generate_static_pix_mock(self, order: Order, company: Company):
        """Gera QR Code estático (Legado/Manual)"""
        # (Lógica simplificada do código antigo para manter compatibilidade)
        return {
            "id": f"manual_{order.id}",
            "status": "pending",
            "qr_code": "000201... (Pix Estático)",
            "qr_code_base64": None
        }