# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models import Order, Company, CustomerWallet
import logging

logger = logging.getLogger("LoyaltyEngine")

class LoyaltyService:
    @staticmethod
    def process_cashback(db: Session, order: Order):
        """
        Calcula e credita o cashback na carteira do cliente após pagamento confirmado.
        """
        if not order.customer_phone:
            return # Sem telefone, sem fidelidade

        company = db.query(Company).filter(Company.id == order.company_id).first()
        if not company or not company.loyalty_percentage or company.loyalty_percentage <= 0:
            return

        # Evitar duplicidade (se já processou, ignora)
        if order.cashback_earned > 0:
            logger.info(f"Cashback já processado para pedido {order.id}")
            return

        # Cálculo do Cashback
        # Regra: O cashback é sobre o valor pago em dinheiro/cartão (total_amount), 
        # não sobre o valor que foi abatido com saldo anterior.
        cashback_value = (order.total_amount * (company.loyalty_percentage / Decimal(100))).quantize(Decimal("0.01"))

        if cashback_value <= 0:
            return

        # Atualizar/Criar Carteira
        wallet = db.query(CustomerWallet).filter(
            CustomerWallet.company_id == company.id,
            CustomerWallet.customer_phone == order.customer_phone
        ).first()

        if not wallet:
            wallet = CustomerWallet(
                company_id=company.id,
                customer_phone=order.customer_phone,
                balance=Decimal(0)
            )
            db.add(wallet)

        # Transação Atômica
        wallet.balance += cashback_value
        order.cashback_earned = cashback_value
        
        db.commit()
        logger.info(f"💰 Cashback de R$ {cashback_value} creditado para {order.customer_phone} (Pedido {order.id})")