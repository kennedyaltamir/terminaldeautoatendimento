import httpx
import os
from typing import Dict, Any
from decimal import Decimal, ROUND_DOWN
from app.services.payment.interfaces import PaymentProviderInterface
from app.models import Order, Company
import logging

logger = logging.getLogger("MercadoPagoProvider")

class MercadoPagoProvider(PaymentProviderInterface):
    BASE_URL = "https://api.mercadopago.com"
    
    def __init__(self):
        self.app_id = os.getenv("MP_APP_ID")
        self.client_secret = os.getenv("MP_CLIENT_SECRET")
        self.redirect_uri = os.getenv("MP_REDIRECT_URI", "http://localhost:3000/admin/settings/payment/callback")

    async def create_pix_payment(self, order: Order, company: Company, split_rules: Dict[str, Any]) -> Dict[str, Any]:
        creds = company.payment_credentials or {}
        access_token = creds.get("access_token")
        
        if not access_token:
            raise ValueError("Loja não conectada ao Mercado Pago")

        # Lógica de Split
        total_val = float(order.total_amount)
        fee_percentage = split_rules.get("fee_percentage", 0)
        
        # Calcula comissão
        app_fee = 0.0
        if fee_percentage > 0:
            fee_decimal = (order.total_amount * (Decimal(fee_percentage) / 100)).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            app_fee = float(fee_decimal)

        payload = {
            "transaction_amount": total_val,
            "description": f"Pedido #{str(order.id)[:8]}",
            "payment_method_id": "pix",
            "payer": {
                "email": "cliente@mesaflow.com",
                "first_name": order.customer_name or "Cliente"
            },
            "notification_url": f"{os.getenv('PUBLIC_API_URL')}/api/webhooks/mercadopago",
            "external_reference": str(order.id)
        }

        if app_fee > 0:
            payload["application_fee"] = app_fee

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Idempotency-Key": str(order.id)
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.BASE_URL}/v1/payments", json=payload, headers=headers)
            if res.status_code != 201:
                logger.error(f"Erro MP: {res.text}")
                raise Exception(f"Erro no Mercado Pago: {res.status_code}")
            
            data = res.json()
            return {
                "id": str(data["id"]),
                "status": data["status"],
                "qr_code": data["point_of_interaction"]["transaction_data"]["qr_code"],
                "qr_code_base64": data["point_of_interaction"]["transaction_data"]["qr_code_base64"]
            }

    async def get_auth_url(self, state: str) -> str:
        return (
            f"https://auth.mercadopago.com.br/authorization"
            f"?client_id={self.app_id}"
            f"&response_type=code"
            f"&platform_id=mp"
            f"&state={state}"
            f"&redirect_uri={self.redirect_uri}"
        )

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        payload = {
            "client_secret": self.client_secret,
            "client_id": self.app_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.BASE_URL}/oauth/token", json=payload)
            if res.status_code != 200:
                raise Exception(f"Falha OAuth MP: {res.text}")
            return res.json()