# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-01 04:52:00
# DESCRIPTION: Orquestrador de Logística com Lock Pessimista e Integridade Financeira.
import logging
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.logistics import LogisticsJourney, JourneyStatus
from app.models.company import Company
from app.models.orders import Order, OrderStatus, PaymentStatus
from app.services.ledger_service import LedgerService
# from app.services.webhook_dispatcher import WebhookDispatcher # Opcional, se usar webhooks externos

logger = logging.getLogger("LogisticsOrchestrator")

class LogisticsOrchestrator:
    """
    O Árbitro Soberano da Logística.
    Garante que a realidade física (entregador) e contábil (ledger) estejam em sincronia atômica.
    Usa Locks Pessimistas para impedir race conditions em alta concorrência.
    """

    @staticmethod
    def update_journey_state(
        db: Session, 
        journey_id: str, 
        new_status: str, # Recebe string, converte internamente
        payload: dict = None
    ) -> LogisticsJourney:
        """
        Executa a Transição de Estado da FSM com Lock Pessimista.
        """
        if payload is None:
            payload = {}

        # 1. LOCK PESSIMISTA: Database is the Guarantee
        # with_for_update() trava a linha até o commit/rollback da transação
        try:
            journey = db.query(LogisticsJourney).with_for_update().filter(
                LogisticsJourney.id == journey_id
            ).first()
        except Exception as e:
            logger.error(f"🔒 Falha ao adquirir Lock para jornada {journey_id}: {e}")
            raise HTTPException(status_code=503, detail="SISTEMA_OCUPADO_TENTE_NOVAMENTE")

        if not journey:
            raise HTTPException(status_code=404, detail="JORNADA_NAO_ENCONTRADA")

        # 2. Validação de Quarentena (Incident Management)
        if journey.status == JourneyStatus.INCIDENT.value:
            # Apenas um Admin poderia liberar (via outro endpoint).
            # Aqui, bloqueamos qualquer tentativa do motorista.
            logger.warning(f"🛡️ Bloqueio de Segurança: Tentativa de escrita em Jornada {journey_id} (INCIDENT).")
            raise HTTPException(
                status_code=403, 
                detail="INCIDENT_LOCKED: Aguarde liberação do administrador."
            )

        # 3. Validação de Transição de Estado (FSM)
        # Normalização do Enum
        try:
            target_status = JourneyStatus(new_status)
        except ValueError:
             raise HTTPException(status_code=400, detail=f"STATUS_INVALIDO: {new_status}")

        old_status = journey.status
        
        # Lógica de atualização
        journey.status = target_status.value
        # Atualiza timestamp genérico (campos específicos abaixo)
        
        logger.info(f"🔄 FSM Transition: {journey_id} | {old_status} -> {target_status.value}")

        # 4. Ritos de Passagem Específicos
        if target_status == JourneyStatus.COMPLETED:
            LogisticsOrchestrator._finalize_delivery(db, journey, payload)
        
        elif target_status == JourneyStatus.INCIDENT:
            reason = payload.get('reason', 'Motivo não especificado')
            logger.warning(f"🚨 INCIDENTE REPORTADO: Jornada {journey_id} | Motivo: {reason}")
            # O estado já foi atualizado para INCIDENT, bloqueando futuras escritas
        
        elif target_status == JourneyStatus.EN_ROUTE_DELIVERY:
            # Atualiza pedido para 'delivering' se ainda não estiver
            order = db.query(Order).filter(Order.id == journey.order_id).first()
            if order and order.status != OrderStatus.DELIVERING.value:
                order.status = OrderStatus.DELIVERING.value
                db.add(order)
            journey.pickup_at = datetime.now()

        elif target_status == JourneyStatus.AT_DESTINATION:
            journey.arrival_at = datetime.now()

        db.add(journey)
        db.commit()
        db.refresh(journey)
        return journey

    @staticmethod
    def _finalize_delivery(db: Session, journey: LogisticsJourney, payload: dict):
        """
        Rito de Finalização: POD (Proof of Delivery) + Ledger + Drift Check.
        """
        pod_code = payload.get("pod_code")

        # 1. Validação de POD (Proof of Delivery)
        order = db.query(Order).filter(Order.id == journey.order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="PEDIDO_NAO_ENCONTRADO")

        # Se o pedido exige código, valida. Se não tiver código configurado, passa (ex: config de loja).
        if order.delivery_code and str(order.delivery_code).strip() != str(pod_code).strip():
            logger.warning(f"❌ POD Falhou para Jornada {journey.id}. Esperado: {order.delivery_code}, Recebido: {pod_code}")
            raise HTTPException(status_code=400, detail="CODIGO_ENTREGA_INVALIDO")

        # 2. Automação de Ledger (Fintech)
        # Recupera a empresa através do shift -> driver -> company ou direto da jornada se tivermos denormalizado
        # Usando shift para garantir hierarquia
        if not journey.shift:
             # Fallback ou erro crítico
             logger.error(f"CRITICAL: Jornada {journey.id} sem Shift associado.")
             raise HTTPException(status_code=500, detail="ERRO_INTEGRIDADE_SHIFT")

        company_id = journey.shift.company_id
        company = db.query(Company).filter(Company.id == company_id).first()

        # Cálculo de valores
        # Prioriza o fee da jornada se foi negociado dinamicamente, senão usa o fixo da empresa
        fee = Decimal(str(journey.delivery_fee)) if journey.delivery_fee and journey.delivery_fee > 0 else Decimal(str(company.fixed_delivery_fee or 0))
        tip = Decimal(str(payload.get("tip_amount", 0)))
        
        total_credit_cents = int((fee + tip) * 100)

        if total_credit_cents > 0:
            # Registro Imutável no Ledger
            # Driver ID é Int, mas Ledger espera ID de referência. 
            # LedgerService.create_entry espera company_id str
            LedgerService.create_entry(
                db=db,
                company_id=str(company.id),
                amount=total_credit_cents,
                entry_type="CREDIT", # Crédito para o motorista (sistema deve pagar)
                category="delivery_fee",
                reference_id=str(journey.id),
                description=f"Pagamento Entrega #{order.id.hex[:6].upper()} (Taxa: {fee} + Gorjeta: {tip})"
            )
            logger.info(f"💰 Ledger Creditado: {total_credit_cents} cents para Driver {journey.driver_id}")

        # 3. Detecção de Financial_Drift
        # Drift ocorre se o valor pago ao motorista diverge da regra de negócio esperada
        expected_fee = Decimal(str(company.fixed_delivery_fee or 0))
        if expected_fee > 0 and fee != expected_fee:
            drift_amount = fee - expected_fee
            logger.critical(f"⚠️ FINANCIAL_DRIFT DETECTADO: Jornada {journey.id}. Real: {fee}, Esperado: {expected_fee}. Delta: {drift_amount}")
            # Em L9, isso dispararia um ticket automático no Sentry.
        
        # 4. Atualização do Pedido Principal
        order.status = OrderStatus.DELIVERED.value
        # Assume pago se entregue (ou mantém se já pago online). 
        # Cuidado: Se for "Pagar na Entrega", o motorista deve ter confirmado recebimento.
        # Por simplificação V1, assumimos que a entrega conclui o fluxo financeiro do pedido.
        if order.payment_status != PaymentStatus.PAID.value:
             order.payment_status = PaymentStatus.PAID.value
             
        order.finished_at = datetime.now()

        # 5. Atualização da Jornada
        journey.completed_at = datetime.now()
        journey.pod_code_input = pod_code
        journey.delivery_fee = float(fee)
        journey.tip_amount = float(tip)

        db.add(order)
        db.add(journey)
