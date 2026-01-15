# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 09:55:00
import httpx
import os
import logging
import asyncio
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("WhatsAppService")

class WhatsAppService:
    """
    Serviço de integração com APIs de WhatsApp (Evolution API / Twilio).
    Hardened v2.3: Correção de sintaxe e resiliência SRE.
    """
    def __init__(self):
        # Configurações Globais (Fallback)
        self.global_api_url = os.getenv("WHATSAPP_API_URL")
        self.global_token = os.getenv("WHATSAPP_API_TOKEN")
        self.global_instance = os.getenv("WHATSAPP_INSTANCE")
        self.timeout = 5.0

    def _get_config(self, company_settings: Optional[Any]) -> Dict[str, Any]:
        """
        Determina qual configuração usar: A da empresa (SaaS White-label) ou a Global.
        """
        if company_settings:
            api_url = getattr(company_settings, "whatsapp_api_url", None)
            instance = getattr(company_settings, "whatsapp_instance", None)
            token = getattr(company_settings, "whatsapp_token", None)

            if api_url and instance and token:
                return {
                    "url": api_url,
                    "instance": instance,
                    "token": token,
                    "enabled": True
                }

        if self.global_api_url and self.global_token and self.global_instance:
            return {
                "url": self.global_api_url,
                "instance": self.global_instance,
                "token": self.global_token,
                "enabled": True
            }

        return {"enabled": False}

    async def _send_http_request(self, phone: str, message: str, config: Dict[str, Any]) -> bool:
        """Método privado para envio real via HTTP com tratamento de erro robusto."""
        if not config.get("enabled"):
            logger.info(f"MOCK_WHATSAPP: {phone} -> {message[:50]}...")
            return True

        # Normalização do número (E.164)
        clean_phone = "".join(filter(str.isdigit, phone))
        if not clean_phone.startswith("55") and len(clean_phone) <= 11:
            clean_phone = f"55{clean_phone}"

        payload = {
            "number": clean_phone,
            "options": {"delay": 1200, "presence": "composing"},
            "textMessage": {"text": message}
        }

        headers = {
            "apikey": config["token"],
            "Content-Type": "application/json"
        }

        url = f"{config['url'].rstrip('/')}/message/sendText/{config['instance']}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                if response.status_code in [200, 201]:
                    logger.info(f"✅ WhatsApp enviado para {clean_phone}")
                    return True
                logger.warning(f"⚠️ Falha API WhatsApp ({response.status_code}): {response.text}")
                return False
            except Exception as e:
                # SRE: Transforma erro crítico em aviso para não quebrar o fluxo transacional
                logger.warning(f"❌ WhatsApp Offline/Timeout: {str(e)}")
                return False

    async def notify_order_ready(self, customer_name: str, phone: str, table_number: str, restaurant_name: str, company_settings: Any = None):
        """Notifica o cliente que o pedido está pronto."""
        if not phone: return False
        config = self._get_config(company_settings)
        msg = (
            f"Olá *{customer_name}*! 👋\n\n"
            f"Seu pedido da *Mesa {table_number}* está pronto! 🍽️\n\n"
            f"Pode vir retirar ou aguarde que nosso staff já está levando. 😋\n\n"
            f"_{restaurant_name}_"
        )
        return await self._send_http_request(phone, msg, config)

    async def notify_delivery_dispatch(self, customer_name: str, phone: str, driver_name: Optional[str], order_id: str, slug: str, company_settings: Any = None):
        """Notifica o cliente que o pedido saiu para entrega."""
        if not phone: return False
        config = self._get_config(company_settings)
        frontend_url = os.getenv("FRONTEND_URL", "https://mesaflow.com.br")
        tracking_url = f"{frontend_url}/{slug}/menu?order={order_id}"

        driver_info = f" com o entregador *{driver_name}*" if driver_name else ""
        msg = (
            f"Olá *{customer_name}*! 🛵\n\n"
            f"Seu pedido acabou de sair para entrega{driver_info}! 🎉\n\n"
            f"📍 *Acompanhe em tempo real:* {tracking_url}"
        )
        return await self._send_http_request(phone, msg, config)
