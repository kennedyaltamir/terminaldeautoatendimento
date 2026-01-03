from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.orm import Session
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
        event = StripeService.construct_event(payload, stripe_signature)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.critical(f"Erro fatal no Webhook Stripe: {e}")
        raise HTTPException(status_code=400, detail="Erro interno webhook")

    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        metadata = data_object.get("metadata", {})
        company_id = metadata.get("company_id")
        subscription_id = data_object.get("subscription")
        
        if company_id:
            company = db.query(Company).filter(Company.id == company_id).first()
            if company:
                company.plan_tier = PlanTier.PRO
                company.stripe_subscription_id = subscription_id
                company.subscription_status = "active"
                db.commit()

    elif event_type == "customer.subscription.updated":
        company = db.query(Company).filter(Company.stripe_subscription_id == data_object["id"]).first()
        if company:
            status = data_object["status"]
            company.subscription_status = status
            
            if status in ["active", "trialing"]:
                company.plan_tier = PlanTier.PRO
            elif status in ["past_due", "unpaid", "canceled"]:
                company.plan_tier = PlanTier.FREE
            
            db.commit()

    elif event_type == "customer.subscription.deleted":
        company = db.query(Company).filter(Company.stripe_subscription_id == data_object["id"]).first()
        if company:
            company.subscription_status = "canceled"
            company.plan_tier = PlanTier.FREE
            company.stripe_subscription_id = None
            db.commit()

    return {"status": "success"}

@router.post("/fiscal/focus")
async def focus_nfe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook para receber atualizações de status da Focus NFe.
    """
    try:
        data = await request.json()
        ref = data.get("ref") # ID do nosso pedido
        status_sefaz = data.get("status_sefaz")
        status = data.get("status")
        
        if not ref:
            return {"status": "ignored", "reason": "no_ref"}
            
        order = db.query(Order).filter(Order.id == ref).first()
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
            # Poderíamos salvar a mensagem de erro em algum log de auditoria
            
        db.commit()
        return {"status": "processed"}
        
    except Exception as e:
        logger.error(f"Erro Webhook Fiscal: {e}")
        return {"status": "error"}