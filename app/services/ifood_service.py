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
    Realiza o polling de eventos e converte pedidos externos para o MesaFlow.
    """
    
    BASE_URL = "https://merchant-api.ifood.com.br"

    def __init__(self):
        self.is_running = False

    async def start_polling(self):
        """Inicia o loop de polling em background."""
        if self.is_running:
            return
        
        self.is_running = True
        logger.info("🚀 [iFood] Middleware de integração iniciado.")
        
        while self.is_running:
            try:
                await self.process_all_companies()
            except Exception as e:
                logger.error(f"❌ [iFood] Erro no loop de polling: {e}")
            
            await asyncio.sleep(30) # Intervalo de 30 segundos conforme boas práticas do iFood

    async def process_all_companies(self):
        """Varre todas as empresas que possuem merchant_id configurado."""
        db = SessionLocal()
        try:
            companies = db.query(Company).filter(Company.ifood_merchant_id != None).all()
            for company in companies:
                await self.poll_merchant_events(db, company)
        finally:
            db.close()

    async def poll_merchant_events(self, db: Session, company: Company):
        """Consulta novos eventos para um merchant específico."""
        if not company.ifood_token:
            return

        headers = {"Authorization": f"Bearer {company.ifood_token}"}
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # 1. Polling de Eventos
                response = await client.get(f"{self.BASE_URL}/order/v1.0/events:polling", headers=headers)
                
                if response.status_code == 204: # Sem novos eventos
                    return
                
                if response.status_code != 200:
                    logger.error(f"⚠️ [iFood] Erro ao consultar eventos para {company.name}: {response.status_code}")
                    return

                events = response.json()
                processed_event_ids = []

                for event in events:
                    event_id = event.get("id")
                    order_id = event.get("orderId")
                    event_code = event.get("code")

                    # 2. Processar apenas novos pedidos (PLACED)
                    if event_code == "PLACED":
                        await self.ingest_order(db, company, order_id, headers)
                    
                    processed_event_ids.append({"id": event_id})

                # 3. Acknowledge (Confirmar recebimento para limpar a fila do iFood)
                if processed_event_ids:
                    await client.post(
                        f"{self.BASE_URL}/order/v1.0/events:acknowledgment",
                        json=processed_event_ids,
                        headers=headers
                    )

            except Exception as e:
                logger.error(f"❌ [iFood] Falha na comunicação com merchant {company.ifood_merchant_id}: {e}")

    async def ingest_order(self, db: Session, company: Company, external_id: str, headers: dict):
        """Busca detalhes do pedido no iFood e salva no MesaFlow."""
        
        # Verificar se já existe para evitar duplicidade
        exists = db.query(Order).filter(Order.external_order_id == external_id).first()
        if exists:
            return

        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.BASE_URL}/order/v1.0/orders/{external_id}", headers=headers)
            if res.status_code != 200:
                return
            
            data = res.json()
            
            # Conversão de iFood para MesaFlow
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
                payment_method=PaymentMethod.ONLINE, # iFood geralmente é online
                payment_status=PaymentStatus.PAID
            )
            
            db.add(new_order)
            db.flush() # Gera o ID do pedido

            # Processar Itens
            for item in data.get("items", []):
                # CORREÇÃO: Realiza join com Category para filtrar por company_id corretamente
                product = db.query(Product).join(Category).filter(
                    Category.company_id == company.id,
                    Product.external_id == item.get("externalId")
                ).first()

                db_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id if product else 1, # Fallback para item genérico (ID 1) se não mapeado
                    quantity=item.get("quantity"),
                    unit_price=Decimal(str(item.get("unitPrice"))),
                    notes=item.get("observations")
                )
                db.add(db_item)

            db.commit()
            
            # Notificar KDS via WebSocket
            await manager.broadcast({
                "type": "new_order",
                "order_id": str(new_order.id),
                "origin": "ifood",
                "customer": new_order.customer_name
            }, company.slug)
            
            logger.info(f"✅ [iFood] Pedido {external_id} injetado com sucesso para {company.name}")

    def _format_address(self, addr: dict) -> str:
        if not addr: return "Retirada no Balcão"
        return f"{addr.get('street')}, {addr.get('number')} - {addr.get('neighborhood')}, {addr.get('city')}"

if __name__ == "__main__":
    # Para teste manual isolado
    service = IfoodService()
    asyncio.run(service.start_polling())
