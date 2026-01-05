import stripe
import os
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Company, PlanTier

# Configuração de Logs para Rastreabilidade Financeira
logger = logging.getLogger("StripeService")
logging.basicConfig(level=logging.INFO)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_PRO_PRICE_ID = os.getenv("STRIPE_PRO_PRICE_ID")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

class StripeService:
    @staticmethod
    def create_checkout_session(company: Company) -> str:
        """
        Gera uma sessão de checkout do Stripe para upgrade de plano.
        """
        try:
            if not STRIPE_PRO_PRICE_ID:
                raise HTTPException(status_code=500, detail="ID do Preço Stripe não configurado (.env)")

            if not company.stripe_customer_id:
                logger.info(f"Criando cliente Stripe para empresa {company.name} ({company.id})")
                customer = stripe.Customer.create(
                    email=company.owner_email,
                    name=company.name,
                    metadata={"company_id": str(company.id), "slug": company.slug}
                )
                company.stripe_customer_id = customer.id

            if company.subscription_status == 'active':
                raise HTTPException(status_code=400, detail="Empresa já possui assinatura ativa.")

            session = stripe.checkout.Session.create(
                customer=company.stripe_customer_id,
                payment_method_types=["card"],
                line_items=[{
                    "price": STRIPE_PRO_PRICE_ID,
                    "quantity": 1,
                }],
                mode="subscription",
                success_url=f"{FRONTEND_URL}/admin/{company.slug}/settings?billing=success",
                cancel_url=f"{FRONTEND_URL}/admin/{company.slug}/settings?billing=cancel",
                metadata={"company_id": str(company.id)},
                subscription_data={
                    "metadata": {"company_id": str(company.id)}
                },
                allow_promotion_codes=True
            )
            return session.url

        except stripe.error.StripeError as e:
            logger.error(f"Erro Stripe Checkout: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro ao comunicar com provedor de pagamento.")
        except Exception as e:
            logger.error(f"Erro Interno Billing: {str(e)}")
            raise e

    @staticmethod
    def create_portal_session(company: Company) -> str:
        """Gera link para o Portal do Cliente."""
        if not company.stripe_customer_id:
            raise HTTPException(status_code=400, detail="Cliente não vinculado ao sistema de pagamento.")

        try:
            session = stripe.billing_portal.Session.create(
                customer=company.stripe_customer_id,
                return_url=f"{FRONTEND_URL}/admin/{company.slug}/settings"
            )
            return session.url
        except stripe.error.StripeError as e:
            logger.error(f"Erro Stripe Portal: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro ao gerar portal de faturamento.")

    @staticmethod
    def construct_event(payload: bytes, sig_header: str):
        """Valida a assinatura do Webhook."""
        try:
            return stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Payload inválido")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Assinatura do webhook inválida")

    @staticmethod
    def process_webhook_event(event: dict, db: Session):
        """
        Processa a lógica de negócio do evento Stripe.
        Isolado para facilitar testes unitários.
        """
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
                    logger.info(f"Upgrade confirmado para empresa {company_id}")

        elif event_type == "customer.subscription.updated":
            # Busca pela subscription ID pois o metadata pode não vir no update
            company = db.query(Company).filter(Company.stripe_subscription_id == data_object["id"]).first()
            if company:
                status = data_object["status"]
                company.subscription_status = status

                if status in ["active", "trialing"]:
                    company.plan_tier = PlanTier.PRO
                elif status in ["past_due", "unpaid", "canceled"]:
                    company.plan_tier = PlanTier.FREE
                
                db.commit()
                logger.info(f"Status de assinatura atualizado: {status} para {company.id}")

        elif event_type == "customer.subscription.deleted":
            company = db.query(Company).filter(Company.stripe_subscription_id == data_object["id"]).first()
            if company:
                company.subscription_status = "canceled"
                company.plan_tier = PlanTier.FREE
                company.stripe_subscription_id = None
                db.commit()
                logger.info(f"Assinatura cancelada para {company.id}")
