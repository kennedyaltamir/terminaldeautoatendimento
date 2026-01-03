import httpx
import os
import unicodedata
from decimal import Decimal, ROUND_DOWN
from app.models import Order, Company
from dotenv import load_dotenv

load_dotenv()

MP_API_URL = "https://api.mercadopago.com/v1"
BASE_URL = os.getenv("PUBLIC_API_URL", "http://localhost:8000")

class PaymentService:
    def _calculate_crc16(self, payload: str) -> str:
        crc = 0xFFFF
        polynomial = 0x1021
        
        for char in payload:
            byte = ord(char)
            crc ^= (byte << 8)
            for _ in range(8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = crc << 1
                crc &= 0xFFFF
        
        return f"{crc:04X}"

    def _normalize_str(self, text: str) -> str:
        if not text: return ""
        normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        return normalized

    def _generate_static_pix(self, amount: Decimal, pix_key: str, merchant_name: str, merchant_city: str = "Brasilia") -> str:
        if not pix_key:
            pix_key = "CHAVE_NAO_CONFIGURADA"
        
        f_amount = f"{amount:.2f}"
        f_name = self._normalize_str(merchant_name)[:25]
        f_city = self._normalize_str(merchant_city)[:15]
        f_key = self._normalize_str(pix_key)

        gui = "br.gov.bcb.pix"
        field_26_00 = f"00{len(gui):02}{gui}"
        field_26_01 = f"01{len(f_key):02}{f_key}"
        field_26 = f"{field_26_00}{field_26_01}"

        payload = (
            f"000201"
            f"26{len(field_26):02}{field_26}"
            f"52040000"
            f"5303986"
            f"54{len(f_amount):02}{f_amount}"
            f"5802BR"
            f"59{len(f_name):02}{f_name}"
            f"60{len(f_city):02}{f_city}"
            f"62070503***"
            f"6304"
        )
        
        crc = self._calculate_crc16(payload)
        return f"{payload}{crc}"

    def calculate_split(self, total_amount: Decimal, fee_percentage: Decimal) -> Decimal:
        if fee_percentage <= 0:
            return Decimal("0.00")
        
        fee = total_amount * (fee_percentage / Decimal("100"))
        return fee.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

    async def create_pix_payment(self, order: Order, company: Company):
        total_val = Decimal(str(order.total_amount))
        
        if not company.mp_access_token:
            print(f"⚠️ AVISO: Gerando Pix Estático para a chave: {company.pix_key}")
            qr_code_payload = self._generate_static_pix(
                amount=total_val, 
                pix_key=company.pix_key,
                merchant_name=company.name
            )
            return {
                "id": f"manual_{order.id}",
                "status": "pending",
                "qr_code": qr_code_payload,
                "qr_code_base64": None
            }

        headers = {
            "Authorization": f"Bearer {company.mp_access_token}",
            "Content-Type": "application/json",
            "X-Idempotency-Key": str(order.id)
        }

        fee_percentage = Decimal(str(company.marketplace_fee_percentage or 0))
        app_fee = self.calculate_split(total_val, fee_percentage)

        notification_url = f"{BASE_URL}/api/webhooks/mercadopago"
        print(f"🔗 Configurando Webhook para: {notification_url} | Split Fee: R$ {app_fee}")

        payload = {
            "transaction_amount": float(total_val),
            "description": f"Pedido #{str(order.id)[:8]} - {company.name}",
            "payment_method_id": "pix",
            "payer": {
                "email": "cliente@email.com", 
                "first_name": order.customer_name or "Cliente",
            },
            "notification_url": notification_url,
            "application_fee": float(app_fee) if app_fee > 0 else None,
            "external_reference": str(order.id)
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{MP_API_URL}/payments",
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code != 201:
                    print(f"❌ Erro MP ({response.status_code}): {response.text}")
                    response.raise_for_status()

                data = response.json()
                
                return {
                    "id": str(data["id"]),
                    "status": data["status"],
                    "qr_code": data["point_of_interaction"]["transaction_data"]["qr_code"],
                    "qr_code_base64": data["point_of_interaction"]["transaction_data"]["qr_code_base64"]
                }
            except Exception as e:
                print(f"❌ Erro Conexão MP: {str(e)}")
                raise e