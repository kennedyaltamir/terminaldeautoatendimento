import httpx
import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("WhatsAppService")

class WhatsAppService:
    def __init__(self):
        # Configurações Globais (Fallback)
        self.global_api_url = os.getenv("WHATSAPP_API_URL")
        self.global_instance = os.getenv("WHATSAPP_INSTANCE")
        self.global_token = os.getenv("WHATSAPP_API_TOKEN")

    def _get_config(self, company_settings: Optional[Any]) -> Dict[str, Any]:
        """
        Determina qual configuração usar: A da empresa (se existir) ou a Global.
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

        if self.global_api_url and self.global_token:
            return {
                "url": self.global_api_url,
                "instance": self.global_instance,
                "token": self.global_token,
                "enabled": True
            }

        return {"enabled": False}

    async def _send_http_request(self, phone: str, message: str, config: Dict[str, Any]):
        """Método privado para envio real via HTTP."""
        if not config.get("enabled"):
            logger.warning(f"⚠️ WhatsApp desativado. Ignorando msg para {phone}.")
            return False

        # Normalização do número
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

        base_url = config["url"].rstrip("/")
        instance = config["instance"]
        url = f"{base_url}/message/sendText/{instance}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                if response.status_code in [200, 201]:
                    logger.info(f"✅ WhatsApp enviado para {clean_phone}")
                    return True
                logger.error(f"❌ Erro API WhatsApp ({response.status_code}): {response.text}")
                return False
            except Exception as e:
                logger.error(f"🔥 Falha crítica no serviço de WhatsApp: {e}")
                return False

    async def notify_order_ready(self, customer_name: str, phone: str, table_number: str, restaurant_name: str, company_settings: Any = None):
        """Notifica que o pedido está pronto."""
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
        """Notifica saída para entrega."""
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

    async def send_test_message(self, company_settings: Any) -> bool:
        """Valida credenciais com mensagem de teste."""
        target_phone = getattr(company_settings, "whatsapp_number", None)
        if not target_phone: return False
        config = self._get_config(company_settings)
        msg = "🤖 *MesaFlow: Teste de Conexão OK!* ✅"
        return await self._send_http_request(target_phone, msg, config)
