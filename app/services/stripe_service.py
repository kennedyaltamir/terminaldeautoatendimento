import stripe
import os
import logging
from fastapi import HTTPException
from app.models import Company

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
        Cria o cliente no Stripe se não existir.
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
            
            # Verifica se já existe assinatura ativa para evitar duplicidade
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
        """
        Gera link para o Portal do Cliente (Troca de cartão, cancelamento, faturas).
        """
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
        """Valida a assinatura do Webhook para garantir segurança."""
        try:
            return stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Payload inválido")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Assinatura do webhook inválida")

    @staticmethod
    def report_usage(company: Company, amount: float):
        """
        Adiciona um valor extra à próxima fatura do cliente no Stripe.
        Usado para cobrar as comissões de vendas em dinheiro.
        """
        if not company.stripe_customer_id or amount <= 0:
            return

        try:
            stripe.InvoiceItem.create(
                customer=company.stripe_customer_id,
                amount=int(amount * 100), # Stripe usa centavos
                currency="brl",
                description="Comissões sobre vendas em Dinheiro/Cartão Físico"
            )
            logger.info(f"Cobrança extra agendada: R$ {amount} para {company.name}")
        except Exception as e:
            logger.error(f"Erro ao reportar uso ao Stripe: {e}")