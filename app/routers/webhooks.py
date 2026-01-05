from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Order, PaymentStatus, OrderStatus, Company, PlanTier, FiscalStatus
from app.websockets import manager
from app.services.stripe_service import StripeService
from app.services.loyalty_service import LoyaltyService
import logging

router = APIRouter()
logger = logging.getLogger("Webhooks")

@router.post("/mercadopago")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook para baixa automática de Pix via Mercado Pago + Fidelidade"""
    try:
        params = request.query_params
        topic = params.get("topic") or params.get("type")
        resource_id = params.get("id") or params.get("data.id")

        if topic == "payment" and resource_id:
            logger.info(f"Recebido pagamento MP ID: {resource_id}")

            order = db.query(Order).filter(Order.mp_payment_id == resource_id).first()

            if order and order.payment_status != PaymentStatus.PAID:
                # 1. Atualizar Status
                order.payment_status = PaymentStatus.PAID
                if order.status == OrderStatus.PENDING:
                    order.status = OrderStatus.ACCEPTED

                db.commit() # Commit parcial para garantir status

                # 2. Processar Fidelidade (Cashback)
                LoyaltyService.process_cashback(db, order)

                # 3. Notificar KDS e Painel
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
    payload = await request.body()

    try:
        # Valida assinatura
        event = StripeService.construct_event(payload, stripe_signature)

        # Processa lógica de negócio
        StripeService.process_webhook_event(event, db)

        return {"status": "success"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.critical(f"Erro fatal no Webhook Stripe: {e}")
        raise HTTPException(status_code=400, detail="Erro interno webhook")

@router.post("/fiscal/focus")
async def focus_nfe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook para receber atualizações de status da Focus NFe.
    """
    try:
        data = await request.json()
        ref = data.get("ref") # ID do nosso pedido
        status = data.get("status")

        if not ref:
            return {"status": "ignored", "reason": "no_ref"}

        # Conversão segura para UUID
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
