
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 10:30:00

from sqlalchemy.orm import Session
from app.models import Order, OrderStatus, PaymentStatus
from app.services.whatsapp_service import WhatsAppService
from app.services.loyalty_service import LoyaltyService
from app.services.webhook_dispatcher import WebhookDispatcher
from app.websockets import manager
from app.core.utils import normalize_enum
from datetime import datetime
from uuid import UUID

class OrderService:
    @staticmethod
    async def update_status(db: Session, order_id: UUID, new_status: OrderStatus, company_slug: str, background_tasks):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order: return None
        
        old_status = order.status
        
        # RFC-009: Normalização Obrigatória
        order.status = normalize_enum(new_status)
        
        if new_status in [OrderStatus.DELIVERED, OrderStatus.CANCELED]:
            order.finished_at = datetime.now()
            
        if new_status == OrderStatus.DELIVERED and order.payment_status == PaymentStatus.PAID.value:
            LoyaltyService.process_cashback(db, order)
            
        db.commit()
        
        # Notificações
        if new_status == OrderStatus.READY and old_status != OrderStatus.READY.value:
            if order.customer_phone:
                ws = WhatsAppService()
                background_tasks.add_task(ws.notify_order_ready, order.customer_name, order.customer_phone, str(order.table.table_number) if order.table else "Balcão", order.company.name, order.company)
        
        background_tasks.add_task(WebhookDispatcher.dispatch, "order.updated", {"id": str(order.id), "status": order.status}, str(order.company_id))
        await manager.broadcast({"type": "order_update", "order_id": str(order.id), "status": order.status}, company_slug)
        
        return order

