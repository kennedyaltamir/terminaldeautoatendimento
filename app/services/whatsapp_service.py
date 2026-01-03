import httpx
import os
import logging
from typing import List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("WhatsAppService")

class WhatsAppService:
    def __init__(self):
        self.api_url = os.getenv("WHATSAPP_API_URL")
        self.api_token = os.getenv("WHATSAPP_API_TOKEN")
        self.enabled = bool(self.api_url and self.api_token)

    async def send_message(self, phone: str, message: str):
        if not self.enabled:
            logger.warning("WhatsApp Service desativado: WHATSAPP_API_URL ou TOKEN não configurados.")
            return False

        clean_phone = "".join(filter(str.isdigit, phone))
        if not clean_phone.startswith("55"):
            clean_phone = f"55{clean_phone}"

        payload = {
            "number": clean_phone,
            "message": message
        }

        headers = {
            "apikey": self.api_token,
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_url}/message/sendText",
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
                return response.status_code in [200, 201]
            except Exception as e:
                logger.error(f"Erro ao enviar WhatsApp: {e}")
                return False

    async def notify_order_ready(self, customer_name: str, phone: str, table_number: str, restaurant_name: str):
        if not phone:
            return False
        
        msg = (
            f"Olá *{customer_name}*! 👋\n\n"
            f"Boas notícias: seu pedido da *Mesa {table_number}* está pronto e saindo da cozinha agora! 🍽️\n\n"
            f"Prepare o apetite! 😋\n"
            f"_{restaurant_name}_"
        )
        return await self.send_message(phone, msg)

    async def notify_low_stock(self, phone: str, ingredient_name: str, affected_products: List[str], current_stock: float, unit: str):
        if not phone:
            return False

        products_list = "\n- ".join(affected_products)
        msg = (
            f"⚠️ *ALERTA DE ESTOQUE CRÍTICO* ⚠️\n\n"
            f"O ingrediente *{ingredient_name}* atingiu o nível zero ({current_stock} {unit}).\n\n"
            f"🚫 *Produtos pausados automaticamente:* \n- {products_list}\n\n"
            f"Por favor, providencie a reposição para reativar as vendas."
        )
        return await self.send_message(phone, msg)