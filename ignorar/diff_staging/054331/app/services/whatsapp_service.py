# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 09:15:00
import httpx
import os
import logging
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("WhatsAppService")

class WhatsAppService:
    """
    Serviço de integração com APIs de WhatsApp (Evolution API / Twilio).
    Hardened v2: Resiliência a falhas de conexão e modo silencioso.
    """
    def __init__(self):
        self.global_api_url = os.getenv("WHATSAPP_API_URL")
        self.global_token = os.getenv("WHATSAPP_API_TOKEN")
        self.timeout = 5.0 # Timeout reduzido para não travar workers

    def _get_config(self, company_settings: Optional[Any]) -> Dict[str, Any]:
        if company_settings:
            api_url = getattr(company_settings, "whatsapp_api_url", None)
            instance = getattr(company_settings, "whatsapp_instance", None)
            token = getattr(company_settings, "whatsapp_token", None)

            if api_url and instance and token:
                return {"url": api_url, "instance": instance, "token": token, "enabled": True}

        if self.global_api_url and self.global_token:
            return {"url": self.global_api_url, "instance": os.getenv("WHATSAPP_INSTANCE"), "token": self.global_token, "enabled": True}

        return {"enabled": False}

    async def _send_http_request(self, phone: str, message: str, config: Dict[str, Any]):
        if not config.get("enabled"):
            logger.info(f"MOCK_WHATSAPP: {phone} -> {message[:30]}...")
            return True

        clean_phone = "".join(filter(str.isdigit, phone))
        payload = {"number": clean_phone, "textMessage": {"text": message}}
        headers = {"apikey": config["token"], "Content-Type": "application/json"}
        url = f"{config['url'].rstrip('/')}/message/sendText/{config['instance']}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                return response.status_code in [200, 201]
            except Exception as e:
                # SRE: Transforma erro crítico em aviso de log para não quebrar o fluxo transacional
                logger.warning(f"WhatsApp Offline: {str(e)}")
                return False

    async def notify_order_ready(self, customer_name: str, phone: str, table_number: str, restaurant_name: str, company_settings: Any = None):
        if not phone: return False
        config = self._get_config(company_settings)
        msg = f"Olá *{customer_name}*! 👋 Seu pedido da *Mesa {table_number}* está pronto! 🍽️"
        return await self._send_http_request(phone, msg, config)

    async def notify_delivery_dispatch(self, customer_name: str, phone: str, driver_name: Optional[str], order_id: str, slug: str, company_settings: Any = None):
        if not phone: return False
        config = self._get_config(company_settings)
        msg = f"Olá *{customer_name}*! 🛵 Seu pedido #{order_id[:6]} saiu para entrega! 🎉"
        return await self._send_http_request(phone, msg, config)
