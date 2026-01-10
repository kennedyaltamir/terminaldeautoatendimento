# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-09 00:20:00
from sqlalchemy.orm import Session
from app.models import Order, Company, PaymentProvider, PaymentTransaction
from app.services.payment.factory import PaymentFactory
from decimal import Decimal, ROUND_DOWN
import logging

logger = logging.getLogger("PaymentService")

class PaymentService:
    def calculate_split(self, total_amount: Decimal, fee_percentage: Decimal) -> Decimal:
        """
        Calcula o valor da comissão (Split) com arredondamento seguro.
        """
        if fee_percentage <= 0:
            return Decimal("0.00")

        # Proteção contra taxas absurdas (>100%)
        if fee_percentage >= 100:
            return (total_amount * Decimal("0.5")).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        fee = (total_amount * (fee_percentage / 100)).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        return fee

    async def create_pix_payment(self, order: Order, company: Company):
        """
        Orquestrador que decide qual provedor usar baseado na configuração da empresa.
        """
        provider_enum = company.payment_provider

        if provider_enum == PaymentProvider.NONE or not provider_enum:
            return self._generate_static_pix_mock(order, company)

        try:
            provider = PaymentFactory.get_provider(provider_enum)
            split_rules = {
                "fee_percentage": float(company.marketplace_fee_percentage or 0)
            }
            return await provider.create_pix_payment(order, company, split_rules)

        except Exception as e:
            logger.error(f"Erro no pagamento ({provider_enum}): {e}")
            raise e

    @staticmethod
    def register_transaction_idempotent(db: Session, company_id: str, order_id: str, provider: PaymentProvider, external_id: str, amount: Decimal) -> bool:
        """
        Tenta registrar uma transação. Retorna True se for nova, False se já existir.
        Garante a integridade financeira (Idempotência).
        """
        existing = db.query(PaymentTransaction).filter(
            PaymentTransaction.provider == provider,
            PaymentTransaction.external_id == external_id
        ).first()

        if existing:
            logger.warning(f"⚠️  Transação duplicada detectada e bloqueada: {provider}:{external_id}")
            return False

        new_tx = PaymentTransaction(
            company_id=company_id,
            order_id=order_id,
            provider=provider,
            external_id=external_id,
            amount=amount,
            status="processed"
        )
        db.add(new_tx)
        return True

    def _generate_static_pix_mock(self, order: Order, company: Company):
        return {
            "id": f"manual_{order.id}",
            "status": "pending",
            "qr_code": "000201... (Pix Estático)",
            "qr_code_base64": None
        }
