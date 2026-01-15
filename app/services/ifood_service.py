
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 10:30:00
import httpx
import asyncio
import logging
import json
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Company, Order, OrderItem, OrderStatus, OrderOrigin, Product, Category, OrderType, PaymentStatus, PaymentMethod
from app.websockets import manager
from app.core.utils import normalize_enum

logger = logging.getLogger("IfoodService")

class IfoodService:
    """
    Middleware de integração com iFood.
    Suporta Polling (Legacy) e Webhooks (New).
    """
    BASE_URL = "https://merchant-api.ifood.com.br"
    POLLING_INTERVAL = 900 # Aumentado para 15min pois agora usamos Webhooks
    
    def __init__(self):
        self.is_running = False

    async def start_polling(self):
        """
        Mantém o polling como FALLBACK de segurança caso o Webhook falhe.
        """
        if self.is_running:
            return
        self.is_running = True
        logger.info(f"🚀 [iFood] Middleware iniciado. Polling de fallback a cada {self.POLLING_INTERVAL}s.")
        while self.is_running:
            try:
                await self.process_all_companies()
            except Exception as e:
                logger.error(f"❌ [iFood] Erro no loop de polling: {repr(e)}")
            await asyncio.sleep(self.POLLING_INTERVAL)

    async def process_all_companies(self):
        db = SessionLocal()
        try:
            companies = db.query(Company).filter(Company.ifood_merchant_id != None).all()
            for company in companies:
                try:
                    await self.poll_merchant_events(db, company)
                except Exception as e:
                    logger.error(f"Erro ao processar empresa {company.name}: {repr(e)}")
        finally:
            db.close()

    async def poll_merchant_events(self, db: Session, company: Company):
        if not company.ifood_token:
            return

        headers = {"Authorization": f"Bearer {str(company.ifood_token).strip()}"}
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.BASE_URL}/order/v1.0/events:polling", headers=headers)
                if response.status_code == 204: 
                    return
                if response.status_code != 200:
                    logger.warning(f"⚠️ [iFood] Erro polling {company.name}: {response.status_code}")
                    return
                
                events = response.json()
                processed_event_ids = []
                
                for event in events:
                    # Reusa a lógica do webhook para processar o evento
                    await self.process_webhook_event(db, event, company)
                    processed_event_ids.append({"id": event.get("id")})
                
                if processed_event_ids:
                    await client.post(
                        f"{self.BASE_URL}/order/v1.0/events:acknowledgment",
                        json=processed_event_ids,
                        headers=headers
                    )
            except Exception as e:
                logger.error(f"❌ [iFood] Falha polling merchant {company.ifood_merchant_id}: {repr(e)}")

    async def process_webhook_event(self, db: Session, event: dict, known_company: Company = None):
        """
        Processa um evento único, vindo do Webhook ou do Polling.
        """
        merchant_id = event.get("merchantId")
        event_code = event.get("code")
        order_id = event.get("orderId")
        
        if not merchant_id:
            return

        # Se não passamos a empresa (Webhook), buscamos no banco
        company = known_company
        if not company:
            company = db.query(Company).filter(Company.ifood_merchant_id == merchant_id).first()
        
        if not company:
            logger.warning(f"[iFood] Merchant ID desconhecido: {merchant_id}")
            return

        logger.info(f"[iFood] Processando evento {event_code} para pedido {order_id}")

        headers = {"Authorization": f"Bearer {str(company.ifood_token).strip()}"}

        if event_code == "PLACED":
            await self.ingest_order(db, company, order_id, headers)
        elif event_code == "CONFIRMED":
            self._update_order_status(db, order_id, OrderStatus.ACCEPTED)
        elif event_code == "DISPATCHED":
            self._update_order_status(db, order_id, OrderStatus.DELIVERING)
        elif event_code == "CONCLUDED":
            self._update_order_status(db, order_id, OrderStatus.DELIVERED)
        elif event_code == "CANCELLED":
            self._update_order_status(db, order_id, OrderStatus.CANCELED)

    async def ingest_order(self, db: Session, company: Company, external_id: str, headers: dict):
        # Idempotência: Se já existe, ignora
        exists = db.query(Order).filter(Order.external_order_id == external_id).first()
        if exists:
            logger.info(f"[iFood] Pedido {external_id} já existe. Ignorando ingestão.")
            return

        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.BASE_URL}/order/v1.0/orders/{external_id}", headers=headers)
            if res.status_code != 200:
                logger.error(f"[iFood] Falha ao buscar detalhes do pedido {external_id}")
                return
            
            data = res.json()
            
            # Mapeamento de endereço
            delivery_data = data.get("delivery", {})
            address_str = self._format_address(delivery_data.get("deliveryAddress", {}))
            
            # Criação do Pedido
            # RFC-009: Normalização de Enums na criação
            new_order = Order(
                company_id=company.id,
                origin=normalize_enum(OrderOrigin.IFOOD),
                external_order_id=external_id,
                order_type=normalize_enum(OrderType.DELIVERY if delivery_data.get("mode") == "DELIVERY" else OrderType.TAKEOUT),
                customer_name=data.get("customer", {}).get("name", "Cliente iFood"),
                customer_phone=data.get("customer", {}).get("phone", {}).get("number"),
                delivery_address=address_str,
                subtotal=Decimal(str(data.get("total", {}).get("subTotal", 0))),
                delivery_fee=Decimal(str(data.get("total", {}).get("deliveryFee", 0))),
                total_amount=Decimal(str(data.get("total", {}).get("orderAmount", 0))),
                status=normalize_enum(OrderStatus.PENDING),
                payment_method=normalize_enum(PaymentMethod.ONLINE if data.get("payments", {}).get("methods", [{}])[0].get("type") == "ONLINE" else PaymentMethod.CASH),
                payment_status=normalize_enum(PaymentStatus.PAID if data.get("payments", {}).get("methods", [{}])[0].get("type") == "ONLINE" else PaymentStatus.PENDING)
            )
            
            db.add(new_order)
            db.flush() # Gera ID
            
            # Itens
            for item in data.get("items", []):
                external_prod_id = item.get("externalCode") or item.get("id")
                
                # Tenta match por código externo ou nome
                product = db.query(Product).join(Category).filter(
                    Category.company_id == company.id,
                    (Product.external_id == external_prod_id) | (Product.name == item.get("name"))
                ).first()
                
                db_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id if product else 1, 
                    quantity=item.get("quantity"),
                    unit_price=Decimal(str(item.get("unitPrice"))),
                    notes=item.get("observations")
                )
                db.add(db_item)
            
            db.commit()
            
            # Notifica KDS
            await manager.broadcast({
                "type": "new_order",
                "order_id": str(new_order.id),
                "origin": "ifood",
                "customer": new_order.customer_name
            }, company.slug)

    def _update_order_status(self, db: Session, external_id: str, new_status: OrderStatus):
        order = db.query(Order).filter(Order.external_order_id == external_id).first()
        if order and order.status != new_status.value:
            # RFC-009: Normalização Obrigatória
            order.status = normalize_enum(new_status)
            
            if new_status == OrderStatus.DELIVERED:
                from datetime import datetime
                order.finished_at = datetime.now()
            db.commit()
            logger.info(f"[iFood] Pedido {external_id} atualizado para {new_status}")
            
            if order.company:
                # Broadcast simplificado (idealmente async)
                pass 

    def _format_address(self, addr: dict) -> str:
        if not addr: return "Retirada no Balcão"
        return f"{addr.get('street')}, {addr.get('number')} - {addr.get('neighborhood')}, {addr.get('city')}"

