# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-14 23:20:00
import httpx
import logging
import asyncio
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Company, Order, OrderItem, OrderStatus, OrderOrigin, Product, OrderType, PaymentStatus, PaymentMethod
from app.websockets import manager
from app.core.utils import normalize_enum

logger = logging.getLogger("IfoodService")

class IfoodService:
    """
    Motor de Integração iFood v2.
    Responsável por autenticação, polling de eventos e ingestão de pedidos.
    """
    BASE_URL = "https://merchant-api.ifood.com.br"

    async def get_token(self, client_id: str, client_secret: str) -> str:
        """Obtém o token de acesso OAuth2 do iFood."""
        url = f"{self.BASE_URL}/authentication/v1.0/oauth/token"
        data = {
            "grantType": "client_credentials",
            "clientId": client_id,
            "clientSecret": client_secret
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(url, data=data)
            res.raise_for_status()
            return res.json()["accessToken"]

    async def poll_events(self, db: Session, company: Company):
        """Realiza o polling de eventos pendentes no iFood."""
        if not company.ifood_token:
            return

        headers = {"Authorization": f"Bearer {company.ifood_token}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                res = await client.get(f"{self.BASE_URL}/order/v1.0/events:polling", headers=headers)
                if res.status_code == 204: return # Sem eventos
                
                events = res.json()
                for event in events:
                    await self.process_event(db, company, event)
                    
                # Confirma recebimento dos eventos (Acknowledgment)
                if events:
                    await client.post(
                        f"{self.BASE_URL}/order/v1.0/events:acknowledgment",
                        json=[{"id": e["id"]} for e in events],
                        headers=headers
                    )
            except Exception as e:
                logger.error(f"Erro no polling iFood para {company.name}: {e}")

    async def process_event(self, db: Session, company: Company, event: dict):
        """Processa um evento individual do iFood."""
        event_code = event.get("code")
        order_id = event.get("orderId")

        if event_code == "PLACED":
            await self.ingest_order(db, company, order_id)
        elif event_code == "CANCELLED":
            self._update_local_status(db, order_id, OrderStatus.CANCELED)
        elif event_code == "CONCLUDED":
            self._update_local_status(db, order_id, OrderStatus.DELIVERED)

    async def ingest_order(self, db: Session, company: Company, external_id: str):
        """Busca detalhes do pedido no iFood e cria no MesaFlow."""
        # Evita duplicidade
        if db.query(Order).filter(Order.external_order_id == external_id).first():
            return

        headers = {"Authorization": f"Bearer {company.ifood_token}"}
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.BASE_URL}/order/v1.0/orders/{external_id}", headers=headers)
            if res.status_code != 200: return
            
            data = res.json()
            
            # Criação do Pedido (Normalizado L6)
            new_order = Order(
                company_id=company.id,
                origin=normalize_enum(OrderOrigin.IFOOD),
                external_order_id=external_id,
                customer_name=data.get("customer", {}).get("name", "Cliente iFood"),
                total_amount=Decimal(str(data.get("total", {}).get("orderAmount", 0))),
                status=normalize_enum(OrderStatus.PENDING),
                order_type=normalize_enum(OrderType.DELIVERY),
                payment_status=normalize_enum(PaymentStatus.PAID if data.get("payments", {}).get("prePaid") else PaymentStatus.PENDING)
            )
            
            db.add(new_order)
            db.commit()
            
            # Notifica KDS em tempo real
            await manager.broadcast({
                "type": "new_order",
                "order_id": str(new_order.id),
                "origin": "ifood",
                "customer": new_order.customer_name
            }, company.slug)

    def _update_local_status(self, db: Session, external_id: str, status: OrderStatus):
        order = db.query(Order).filter(Order.external_order_id == external_id).first()
        if order:
            order.status = normalize_enum(status)
            db.commit()
