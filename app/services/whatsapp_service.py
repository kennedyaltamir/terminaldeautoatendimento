# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-23 23:15:00
# DESCRIPTION: Serviço de mensageria com Circuit Breaker e Fallback Silencioso.
import httpx
import os
import logging
import asyncio
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("WhatsAppService")

class WhatsAppService:
    """
    Serviço de integração com APIs de WhatsApp (Evolution API / WppConnect).
    Suporta configurações globais (.env) ou específicas por Tenant (DB).
    Implementa Circuit Breaker para evitar travamento de threads em caso de falha da API externa.
    """
    def __init__(self):
        self.global_api_url = os.getenv("WHATSAPP_API_URL")
        self.global_token = os.getenv("WHATSAPP_API_TOKEN")
        self.global_instance = os.getenv("WHATSAPP_INSTANCE")
        self.timeout = 5.0 # Timeout reduzido para falhar rápido
        self.circuit_open = False
        self.last_failure = 0
        self.retry_after = 60 # Segundos para reabrir o circuito

    def _extract_value(self, source: Any, key: str) -> Optional[str]:
        """Helper agnóstico para extrair valores de Objetos ou Dicionários."""
        if source is None:
            return None
        if isinstance(source, dict):
            return source.get(key)
        if hasattr(source, key):
            return getattr(source, key)
        return None

    def _get_config(self, company_settings: Any) -> Dict[str, Any]:
        """
        Resolve a configuração de API, priorizando o Tenant e caindo para o Global (Env).
        """
        if company_settings:
            api_url = self._extract_value(company_settings, "whatsapp_api_url")
            instance = self._extract_value(company_settings, "whatsapp_instance")
            token = self._extract_value(company_settings, "whatsapp_token")
            
            if api_url and instance and token:
                return {
                    "url": str(api_url).rstrip("/"),
                    "instance": str(instance).strip(),
                    "token": str(token).strip(),
                    "enabled": True
                }
        return self._get_global_config()

    def _get_global_config(self) -> Dict[str, Any]:
        if self.global_api_url and self.global_token and self.global_instance:
            return {
                "url": self.global_api_url.rstrip("/"),
                "instance": self.global_instance,
                "token": self.global_token,
                "enabled": True
            }
        return {"enabled": False}

    async def _send_http_request(self, phone: str, message: str, config: Dict[str, Any]) -> bool:
        """Executa o envio HTTP com Circuit Breaker e tratamento de exceção robusto."""
        if not config.get("enabled"):
            logger.info(f"📱 [MOCK WA] Para: {phone} | Msg: {message[:50]}...")
            return True

        # Circuit Breaker Check
        if self.circuit_open:
            if (asyncio.get_event_loop().time() - self.last_failure) > self.retry_after:
                self.circuit_open = False # Tenta novamente (Half-Open)
                logger.info("🔄 WhatsApp Circuit Breaker: Tentando recuperação...")
            else:
                logger.warning("⚠️ WhatsApp Circuit Open: Skipping request.")
                return False

        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith("55") and len(clean_phone) <= 11:
            clean_phone = f"55{clean_phone}"

        payload = {
            "number": clean_phone,
            "textMessage": {"text": message},
            "options": {"delay": 1200, "presence": "composing"}
        }
        
        headers = {
            "apikey": config["token"], 
            "Content-Type": "application/json"
        }
        
        url = f"{config['url']}/message/sendText/{config['instance']}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                if response.status_code in [200, 201]:
                    return True
                
                logger.warning(f"⚠️ WhatsApp API Error ({response.status_code}): {response.text[:200]}")
                return False

            except (httpx.RequestError, httpx.ConnectError, httpx.TimeoutException) as e:
                logger.error(f"❌ WhatsApp Network Error: {str(e)}")
                self.circuit_open = True
                self.last_failure = asyncio.get_event_loop().time()
                return False
            except Exception as e:
                logger.error(f"❌ WhatsApp Unexpected Error: {str(e)}")
                return False

    async def notify_order_ready(self, customer_name: str, phone: str, table_number: str, restaurant_name: str, company_settings: Any = None):
        if not phone: return False
        config = self._get_config(company_settings)
        
        msg = (
            f"Olá *{customer_name or 'Cliente'}*! 👋\n\n"
            f"Seu pedido da *{table_number}* está pronto! 🍽️\n"
            f"Por favor, retire no balcão.\n\n"
            f"_{restaurant_name}_"
        )
        return await self._send_http_request(phone, msg, config)

    async def notify_low_stock(self, phone: str, ingredient_name: str, affected_products: list, current_stock: float, unit: str, company_settings: Any = None):
        if not phone: return False
        config = self._get_config(company_settings)
        
        prods_str = "\n- ".join(affected_products[:5])
        msg = (
            f"⚠️ *ALERTA DE ESTOQUE BAIXO*\n\n"
            f"O insumo *{ingredient_name}* atingiu o nível crítico.\n"
            f"Estoque atual: {current_stock} {unit}\n\n"
            f"Produtos afetados (pausados):\n- {prods_str}"
        )
        return await self._send_http_request(phone, msg, config)

    async def notify_delivery_dispatch(self, customer_name: str, phone: str, driver_name: Optional[str], order_id: str, slug: str, company_settings: Any = None):
        if not phone: return False
        config = self._get_config(company_settings)
        
        msg = (
            f"Olá *{customer_name or 'Cliente'}*! 🛵\n\n"
            f"Seu pedido *#{order_id[:4].upper()}* saiu para entrega!\n"
        )
        if driver_name:
            msg += f"Entregador: {driver_name}\n"
            
        base_domain = os.getenv("NEXT_PUBLIC_ROOT_DOMAIN", "localhost:3000")
        protocol = "https" if "localhost" not in base_domain else "http"
        tracking_link = f"{protocol}://{base_domain}/{slug}/menu?order={order_id}"
        
        msg += f"\nAcompanhe aqui: {tracking_link}"
        
        return await self._send_http_request(phone, msg, config)
