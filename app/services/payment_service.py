# DOMAIN: BACKEND / FINTECH
# OBJECTIVE: Geração de Pix Real e Processamento de Webhooks.
# FEATURES: Payload EMV, Idempotência e Validação de Valor.
from sqlalchemy.orm import Session
from app.models import Order, Company, PaymentProvider, PaymentTransaction, OrderStatus, PaymentStatus
from app.services.payment.factory import PaymentFactory
from app.websockets import manager
from decimal import Decimal, ROUND_DOWN
import logging
import uuid

logger = logging.getLogger("PaymentService")

class PaymentService:
    """
    Orquestrador Financeiro do MesaFlow.
    Garante que a criação do pedido e a transação no gateway sejam síncronas no banco.
    """

    async def create_pix_payment(self, db: Session, order: Order, company: Company):
        """
        Gera a cobrança Pix e persiste a transação imediatamente.
        """
        provider_enum = company.payment_provider
        
        # 1. Resolução do Provedor (Real ou Mock)
        if provider_enum == PaymentProvider.NONE or not provider_enum:
            # Mock para testes locais ou sem provedor configurado
            pix_data = self._generate_static_pix_mock(order, company)
            provider = PaymentProvider.NONE
        else:
            try:
                factory_provider = PaymentFactory.get_provider(provider_enum)
                split_rules = {"fee_percentage": float(company.marketplace_fee_percentage or 0)}
                
                # Chamada ao Gateway Real
                pix_data = await factory_provider.create_pix_payment(order, company, split_rules)
                provider = provider_enum
            except Exception as e:
                logger.error(f"Erro no provedor {provider_enum}: {e}")
                raise e

        # 2. Registro de Idempotência (Persistência da Intenção de Pagamento)
        self.register_transaction_idempotent(
            db, 
            str(order.company_id), 
            str(order.id), 
            provider, 
            pix_data["id"], 
            order.total_amount
        )

        # 3. Sincronização de Metadados no Pedido
        order.mp_payment_id = pix_data["id"]
        order.mp_qr_code = pix_data.get("qr_code")
        order.mp_qr_code_base64 = pix_data.get("qr_code_base64")
        
        # Commit da transação Pix no objeto Order
        db.add(order)
        db.commit()
        
        return pix_data

    @staticmethod
    def register_transaction_idempotent(db: Session, company_id: str, order_id: str, provider: PaymentProvider, external_id: str, amount: Decimal) -> bool:
        existing = db.query(PaymentTransaction).filter(
            PaymentTransaction.provider == provider,
            PaymentTransaction.external_id == external_id
        ).first()
        
        if existing:
            logger.warning(f"⚠️ Transação duplicada detectada: {external_id}")
            return False
            
        new_tx = PaymentTransaction(
            id=uuid.uuid4(),
            company_id=company_id,
            order_id=order_id,
            provider=provider,
            external_id=external_id,
            amount=amount,
            status="pending"
        )
        db.add(new_tx)
        db.flush() # Garante que o registro exista para o Webhook sem fechar a transação principal se houver
        return True

    @staticmethod
    async def process_pix_webhook(db: Session, external_id: str, status: str, amount: float):
        """
        Processa a confirmação do banco e libera o pedido para a cozinha.
        """
        transaction = db.query(PaymentTransaction).filter(
            PaymentTransaction.external_id == external_id
        ).first()

        if not transaction:
            logger.error(f"⚠️ Webhook órfão: Transação {external_id} não encontrada.")
            return False

        if transaction.status == "paid":
            logger.info(f"Transação {external_id} já paga. Ignorando duplicidade.")
            return True

        # Validação de Integridade de Valor (Anti-Fraude)
        # Tolerância de 1 centavo para erros de arredondamento float
        if abs(float(transaction.amount) - amount) > 0.01:
            logger.critical(f"🚨 FRAUDE DETECTADA: Valor divergente na transação {external_id}. Esperado: {transaction.amount}, Recebido: {amount}")
            transaction.status = "fraud_suspect"
            db.commit()
            return False

        if status == "approved":
            transaction.status = "paid"
            
            order = db.query(Order).filter(Order.id == transaction.order_id).first()
            if order:
                order.payment_status = PaymentStatus.PAID.value
                
                # Auto-aceite para Kiosk (Agilidade Operacional)
                # Se veio do Kiosk e pagou, já vai pra cozinha (Accepted/Preparing)
                if order.origin == "kiosk" and order.status == OrderStatus.PENDING.value:
                    order.status = OrderStatus.ACCEPTED.value
                
                db.commit()

                # Notificação Real-time para todos os terminais (KDS, Garçom, Cliente)
                if order.company:
                    await manager.broadcast({
                        "type": "payment_confirmed",
                        "order_id": str(order.id),
                        "new_status": order.status,
                        "pickup_note": order.pickup_note,
                        "amount": float(order.total_amount)
                    }, order.company.slug)
                
                return True
        
        return False

    def _generate_static_pix_mock(self, order: Order, company: Company):
        """Gera dados falsos para teste local quando não há provedor configurado."""
        return {
            "id": f"manual_{order.id}",
            "status": "pending",
            "qr_code": "00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000520400005303986540510.005802BR5913Fulano de Tal6008BRASILIA62070503***6304ABCD",
            "qr_code_base64": None # Frontend deve gerar o QR visualmente se base64 for null
        }
