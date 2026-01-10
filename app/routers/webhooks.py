# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-09 00:20:00
from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Order, PaymentStatus, OrderStatus, Company, PlanTier, FiscalStatus, PaymentProvider
from app.websockets import manager
from app.services.stripe_service import StripeService
from app.services.loyalty_service import LoyaltyService
from app.services.payment_service import PaymentService
import logging

router = APIRouter()
logger = logging.getLogger("Webhooks")
payment_service = PaymentService()

@router.post("/mercadopago")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook Hardened para baixa automática via Mercado Pago com Idempotência"""
    try:
        params = request.query_params
        topic = params.get("topic") or params.get("type")
        resource_id = params.get("id") or params.get("data.id")

        if topic == "payment" and resource_id:
            logger.info(f"Recebido pagamento MP ID: {resource_id}")

            order = db.query(Order).filter(Order.mp_payment_id == resource_id).first()

            if order and order.payment_status != PaymentStatus.PAID:
                # 🛡️ TRAVA DE IDEMPOTÊNCIA (FINTECH)
                is_new = payment_service.register_transaction_idempotent(
                    db, 
                    str(order.company_id), 
                    str(order.id), 
                    PaymentProvider.MERCADO_PAGO, 
                    str(resource_id), 
                    order.total_amount
                )

                if not is_new:
                    return {"status": "already_processed"}

                # 1. Atualizar Status
                order.payment_status = PaymentStatus.PAID
                if order.status == OrderStatus.PENDING:
                    order.status = OrderStatus.ACCEPTED

                db.commit() 

                # 2. Processar Fidelidade (Cashback)
                LoyaltyService.process_cashback(db, order)

                # 3. Notificar Real-time
                if order.company:
                    await manager.broadcast({
                        "type": "order_update",
                        "order_id": str(order.id),
                        "status": order.status,
                        "payment_status": order.payment_status,
                        "origin": "webhook_mp"
                    }, order.company.slug)

                return {"status": "processed"}

        return {"status": "ignored"}
    except Exception as e:
        logger.error(f"Erro Webhook MP: {e}")
        return {"status": "error"}

@router.post("/stripe")
async def stripe_webhook(
    request: Request, 
    stripe_signature: str = Header(None), 
    db: Session = Depends(get_db)
):
    """Webhook para Stripe com validação de assinatura"""
    payload = await request.body()

    try:
        event = StripeService.construct_event(payload, stripe_signature)
        
        # Idempotência do Stripe é tratada internamente pelo StripeService 
        # ou pode ser adicionada aqui similar ao MP para eventos de PaymentIntent.
        StripeService.process_webhook_event(event, db)

        return {"status": "success"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.critical(f"Erro fatal no Webhook Stripe: {e}")
        raise HTTPException(status_code=400, detail="Erro interno webhook")

@router.post("/fiscal/focus")
async def focus_nfe_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook para atualizações de status fiscal"""
    try:
        data = await request.json()
        ref = data.get("ref") 
        status = data.get("status")

        if not ref:
            return {"status": "ignored", "reason": "no_ref"}

        try:
            order_uuid = UUID(ref)
        except ValueError:
            return {"status": "ignored", "reason": "invalid_ref_uuid"}

        order = db.query(Order).filter(Order.id == order_uuid).first()
        if not order:
            return {"status": "ignored", "reason": "order_not_found"}

        logger.info(f"Webhook Fiscal recebido para Pedido {ref}: {status}")

        if status == "autorizado":
            order.fiscal_status = FiscalStatus.EMITTED
            order.nfe_key = data.get("chave_nfe")
            order.nfe_url_pdf = data.get("url_danfe")
            order.nfe_url_xml = data.get("url_xml")
        elif status == "erro_autorizacao":
            order.fiscal_status = FiscalStatus.ERROR

        db.commit()
        return {"status": "processed"}

    except Exception as e:
        logger.error(f"Erro Webhook Fiscal: {e}")
        return {"status": "error"}
