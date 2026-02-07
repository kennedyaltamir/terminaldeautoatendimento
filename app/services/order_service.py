import math
import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, BackgroundTasks

from app.models.orders import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.menu import Product
from app.models.auth import Employee
from app.schemas.orders import OrderCreate
from app.core.utils import normalize_enum
from app.websockets import manager
from app.services.whatsapp_service import WhatsAppService
from app.services.loyalty_service import LoyaltyService
from app.services.webhook_dispatcher import WebhookDispatcher

class OrderService:
    """
    Sovereign Order Orchestrator.
    Gerencia o ciclo de vida completo do pedido, garantindo que a transição de estados
    seja atômica, auditável e sincronizada em tempo real com todos os terminais.
    """

    @staticmethod
    def calculate_haversine_eta(curr_lat: float, curr_lng: float, dest_lat: float, dest_lng: float) -> int:
        """
        Enterprise ETA Model (Haversine).
        Calcula o tempo estimado de chegada baseado na curvatura da terra e velocidade média urbana.
        """
        R = 6371000.0  # Raio da Terra em metros
        phi1, phi2 = math.radians(curr_lat), math.radians(dest_lat)
        dphi = math.radians(dest_lat - curr_lat)
        dlambda = math.radians(dest_lng - curr_lng)
        
        a = (math.sin(dphi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        if distance <= 0: return 60
        
        speed_mps = 5.5  # ~20km/h média urbana
        return int((distance / speed_mps) * 1.25)  # 25% buffer para tráfego

    @staticmethod
    async def create_order(
        db: Session, 
        company_id: UUID, 
        data: OrderCreate, 
        origin: str, 
        order_type: str, 
        background_tasks: BackgroundTasks
    ) -> Order:
        """
        Rito de Criação Atômica.
        Valida preços, mapeia itens e dispara o sinal de 'Novo Pedido' para o ecossistema.
        """
        new_order = Order(
            id=uuid.uuid4(),
            company_id=company_id,
            table_id=data.table_id,
            customer_name=data.customer_name,
            customer_phone=data.customer_phone,
            delivery_address=data.delivery_address,
            pickup_note=data.pickup_note,
            order_type=normalize_enum(order_type),
            origin=normalize_enum(origin),
            payment_method=normalize_enum(data.payment_method),
            status=OrderStatus.PENDING.value,
            payment_status=PaymentStatus.PENDING.value,
            total_amount=Decimal("0.00"),
            created_at=datetime.utcnow()
        )
        db.add(new_order)
        db.flush()  # Gera ID para os itens

        total = Decimal("0.00")
        product_ids = [item.product_id for item in data.items]
        products = db.query(Product).filter(Product.id.in_(product_ids)).all()
        product_map = {p.id: p for p in products}

        for item_data in data.items:
            product = product_map.get(item_data.product_id)
            if not product: continue
            
            unit_price = product.price
            item_total = unit_price * item_data.quantity
            total += item_total

            db_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=unit_price,
                notes=item_data.notes
            )
            db.add(db_item)

        new_order.total_amount = total
        db.commit()
        db.refresh(new_order)

        # Notificação Real-time (KDS / Admin)
        company_slug = new_order.company.slug if new_order.company else "unknown"
        payload = {
            "type": "new_order",
            "order_id": str(new_order.id),
            "status": new_order.status,
            "customer": new_order.customer_name,
            "origin": origin,
            "total": float(total)
        }
        await manager.broadcast(payload, company_slug)
        
        if background_tasks:
            background_tasks.add_task(WebhookDispatcher.dispatch, "order.created", payload, str(company_id))

        return new_order

    @staticmethod
    async def update_status(
        db: Session, 
        order_id: UUID, 
        new_status: str, 
        slug: str, 
        company_id: UUID, 
        background_tasks: BackgroundTasks
    ) -> Optional[Order]:
        """
        Sovereign State Machine.
        Implementa Lock Pessimista para evitar concorrência na cozinha e dispara ritos de conclusão.
        """
        # 🛡️ LOCK PESSIMISTA: Garante que apenas um processo altere o estado por vez
        order = db.query(Order).with_for_update().filter(
            Order.id == order_id, 
            Order.company_id == company_id
        ).first()
        
        if not order: return None
        
        old_status = order.status
        order.status = normalize_enum(new_status)
        
        # Rito de Finalização
        if order.status in ['delivered', 'cancelled']:
            order.finished_at = datetime.utcnow()
            
        # Rito de Cashback (Apenas se entregue e pago)
        if order.status == 'delivered' and order.payment_status == 'paid':
            background_tasks.add_task(LoyaltyService.process_cashback, db, order)
            
        db.commit()
        db.refresh(order)
        
        # Broadcast de Mudança de Estado
        payload = {
            "type": "order_update", 
            "order_id": str(order.id), 
            "status": order.status,
            "customer": order.customer_name,
            "table": order.table.table_number if order.table else "Delivery"
        }
        await manager.broadcast(payload, slug)
        
        # Notificação Ativa ao Cliente (WhatsApp)
        if order.status == 'ready' and old_status != 'ready':
            if order.customer_phone:
                ws = WhatsAppService()
                background_tasks.add_task(
                    ws.notify_order_ready, 
                    order.customer_name, 
                    order.customer_phone, 
                    f"Mesa {order.table.table_number}" if order.table else "Balcão",
                    order.company.name,
                    order.company
                )
                
        background_tasks.add_task(WebhookDispatcher.dispatch, "order.updated", payload, str(company_id))
        return order

    @staticmethod
    async def dispatch_order(db: Session, order_id: UUID, slug: str, employee: Employee, background_tasks: BackgroundTasks):
        """Vincula um entregador ao pedido e inicia a rota."""
        order = db.query(Order).with_for_update().filter(
            Order.id == order_id, 
            Order.company_id == employee.company_id
        ).first()
        
        if not order: raise HTTPException(404, "Pedido não encontrado")
        
        order.status = "delivering"
        order.driver_id = employee.id
        db.commit()
        
        payload = {"type": "order_update", "order_id": str(order.id), "status": "delivering"}
        await manager.broadcast(payload, slug)
        return order

    @staticmethod
    async def update_location(db: Session, order_id: UUID, slug: str, lat: float, lng: float, company_id: UUID):
        """Propaga a localização do entregador em tempo real via WebSocket."""
        order = db.query(Order).filter(Order.id == order_id, Order.company_id == company_id).first()
        if not order: raise HTTPException(404, "Pedido não encontrado")
        
        # Destino (Coordenadas da Loja ou Cliente - Exemplo fixo para demonstração)
        dest_lat, dest_lng = -19.22815, -44.94195
        eta_seconds = OrderService.calculate_haversine_eta(lat, lng, dest_lat, dest_lng)
        
        await manager.broadcast({
            "type": "DELIVERY_LOCATION",
            "order_id": str(order_id),
            "payload": {
                "lat": lat,
                "lng": lng,
                "eta_seconds": eta_seconds,
                "timestamp": datetime.utcnow().isoformat()
            }
        }, slug)
        return {"status": "propagated", "eta_seconds": eta_seconds}

    @staticmethod
    async def get_active_orders(db: Session, company_id: UUID) -> List[Order]:
        """Recupera pedidos em fila de produção."""
        return db.query(Order).filter(
            and_(
                Order.company_id == company_id,
                Order.status.in_(['pending', 'preparing', 'ready'])
            )
        ).order_by(Order.created_at.asc()).all()

    @staticmethod
    async def get_recent_completed_orders(db: Session, company_id: UUID) -> List[Order]:
        """Recupera histórico imediato (últimas 2 horas)."""
        time_threshold = datetime.utcnow() - timedelta(hours=2)
        return db.query(Order).filter(
            and_(
                Order.company_id == company_id,
                Order.status.in_(['delivered', 'cancelled']),
                Order.finished_at >= time_threshold
            )
        ).order_by(Order.finished_at.desc()).limit(20).all()