# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 08:40:00
import httpx
import os
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger("WhatsAppService")

class WhatsAppService:
    def __init__(self):
        self.global_api_url = os.getenv("WHATSAPP_API_URL")
        self.global_token = os.getenv("WHATSAPP_API_TOKEN")
        self.timeout = 10.0

    def _get_config(self, company_settings: Any) -> Dict[str, Any]:
        api_url = getattr(company_settings, "whatsapp_api_url", None) or self.global_api_url
        token = getattr(company_settings, "whatsapp_token", None) or self.global_token
        instance = getattr(company_settings, "whatsapp_instance", None)
        
        return {
            "url": api_url,
            "token": token,
            "instance": instance,
            "enabled": bool(api_url and token and instance)
        }

    async def _send_http_request(self, phone: str, message: str, config: Dict[str, Any]):
        if not config["enabled"]:
            logger.info(f"MOCK WHATSAPP to {phone}: {message}")
            return True

        url = f"{config['url'].rstrip('/')}/message/sendText/{config['instance']}"
        headers = {"apikey": config["token"], "Content-Type": "application/json"}
        payload = {"number": phone, "textMessage": {"text": message}}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                res = await client.post(url, json=payload, headers=headers)
                return res.status_code in [200, 201]
            except Exception as e:
                logger.error(f"WhatsApp API Error: {e}")
                return False

    async def notify_delivery_dispatch(self, customer_name: str, phone: str, driver_name: Optional[str], order_id: str, slug: str, company_settings: Any):
        config = self._get_config(company_settings)
        msg = f"Olá {customer_name}! Seu pedido #{order_id[:6]} saiu para entrega! 🛵"
        await self._send_http_request(phone, msg, config)

    async def notify_order_ready(self, customer_name: str, phone: str, table_number: str, restaurant_name: str, company_settings: Any):
        config = self._get_config(company_settings)
        msg = f"Olá {customer_name}! Seu pedido da Mesa {table_number} está pronto! 🍽️"
        await self._send_http_request(phone, msg, config)
