# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-10 02:20:00
import httpx
import asyncio
import logging
import json
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Company, Order, OrderItem, OrderStatus, OrderOrigin, Product, Category, OrderType, PaymentStatus, PaymentMethod
from app.websockets import manager

logger = logging.getLogger("IfoodService")

class IfoodService:
    """
    Middleware de integração com iFood.
    Suporta Webhooks (Push) e Polling (Pull/Fallback).
    """
    BASE_URL = "https://merchant-api.ifood.com.br"
    POLLING_INTERVAL = 900 

    def __init__(self):
        self.is_running = False

    async def start_polling(self):
        """Inicia o loop de polling em background (Modo Fallback)."""
        if self.is_running:
            return
        self.is_running = True
        logger.info(f"🚀 [iFood] Middleware iniciado. Polling a cada {self.POLLING_INTERVAL}s.")
        while self.is_running:
            try:
                await self.process_all_companies()
            except Exception as e:
                # Tratamento de erro de encoding e outros erros de loop
                # Forçamos a decodificação segura se for um erro de sistema
                try:
                    error_msg = str(e)
                except UnicodeDecodeError:
                    error_msg = repr(e)
                logger.error(f"❌ [iFood] Erro no loop de polling: {error_msg}")
            await asyncio.sleep(self.POLLING_INTERVAL)

    async def process_all_companies(self):
        """Varre todas as empresas que possuem merchant_id configurado."""
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
        """Consulta novos eventos para um merchant específico (Polling)."""
        if not company.ifood_token:
            return
        
        # Garantir que o token seja tratado como string limpa e segura
        try:
            token = str(company.ifood_token).strip()
            headers = {"Authorization": f"Bearer {token}"}
        except Exception as e:
            logger.error(f"Erro ao processar token iFood para {company.name}: {repr(e)}")
            return
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.BASE_URL}/order/v1.0/events:polling", headers=headers)
                if response.status_code == 204: 
                    return
                if response.status_code != 200:
                    logger.error(f"⚠️ [iFood] Erro ao consultar eventos para {company.name}: {response.status_code}")
                    return
                
                events = response.json()
                processed_event_ids = []
                for event in events:
                    await self.process_single_event(db, company, event, headers)
                    processed_event_ids.append({"id": event.get("id")})

                if processed_event_ids:
                    await client.post(
                        f"{self.BASE_URL}/order/v1.0/events:acknowledgment",
                        json=processed_event_ids,
                        headers=headers
                    )
            except Exception as e:
                logger.error(f"❌ [iFood] Falha na comunicação com merchant {company.ifood_merchant_id}: {repr(e)}")

    async def process_webhook_event(self, db: Session, event: dict):
        merchant_id = event.get("merchantId")
        if not merchant_id:
            return
        company = db.query(Company).filter(Company.ifood_merchant_id == merchant_id).first()
        if not company:
            return
        
        try:
            token = str(company.ifood_token).strip()
            headers = {"Authorization": f"Bearer {token}"}
            await self.process_single_event(db, company, event, headers)
        except Exception as e:
            logger.error(f"Erro no processamento de webhook iFood: {repr(e)}")

    async def process_single_event(self, db: Session, company: Company, event: dict, headers: dict):
        order_id = event.get("orderId")
        event_code = event.get("code")
        if event_code == "PLACED":
            await self.ingest_order(db, company, order_id, headers)

    async def ingest_order(self, db: Session, company: Company, external_id: str, headers: dict):
        exists = db.query(Order).filter(Order.external_order_id == external_id).first()
        if exists:
            return

        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.BASE_URL}/order/v1.0/orders/{external_id}", headers=headers)
            if res.status_code != 200:
                return
            
            data = res.json()
            new_order = Order(
                company_id=company.id,
                origin=OrderOrigin.IFOOD,
                external_order_id=external_id,
                order_type=OrderType.DELIVERY,
                customer_name=data.get("customer", {}).get("name", "Cliente iFood"),
                customer_phone=data.get("customer", {}).get("phone", {}).get("number"),
                delivery_address=self._format_address(data.get("delivery", {}).get("deliveryAddress", {})),
                subtotal=Decimal(str(data.get("total", {}).get("subTotal", 0))),
                delivery_fee=Decimal(str(data.get("total", {}).get("deliveryFee", 0))),
                total_amount=Decimal(str(data.get("total", {}).get("orderAmount", 0))),
                status=OrderStatus.PENDING,
                payment_method=PaymentMethod.ONLINE,
                payment_status=PaymentStatus.PAID
            )
            db.add(new_order)
            db.flush()

            for item in data.get("items", []):
                product = db.query(Product).join(Category).filter(
                    Category.company_id == company.id,
                    Product.external_id == item.get("externalId")
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
            await manager.broadcast({
                "type": "new_order",
                "order_id": str(new_order.id),
                "origin": "ifood",
                "customer": new_order.customer_name
            }, company.slug)

    def _format_address(self, addr: dict) -> str:
        if not addr: return "Retirada no Balcão"
        return f"{addr.get('street')}, {addr.get('number')} - {addr.get('neighborhood')}, {addr.get('city')}"
