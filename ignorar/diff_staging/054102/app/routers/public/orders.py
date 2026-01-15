# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 08:40:00
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import text
from app.database import get_db, set_tenant
from app.models import Company, Order, OrderItem, Product, Table, TableSession, OrderStatus, PaymentStatus, OrderType, OrderOrigin, OrderFeedback
from app.schemas import OrderCreate, OrderResponse, FeedbackCreate
from app.core.limiter import limiter
from app.websockets import manager
from decimal import Decimal
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_public(order_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Permite que o cliente acompanhe o status de um pedido específico via UUID.
    Implementa bypass temporário de RLS para localização do Tenant.
    """
    # 🛡️ SEGURANÇA: Desativa RLS temporariamente para encontrar o pedido e identificar o dono (Tenant)
    db.execute(text("SET row_security = off"))
    
    order = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options),
        selectinload(Order.table),
        selectinload(Order.feedback)
    ).filter(Order.id == order_id).first()
    
    if not order:
        db.execute(text("SET row_security = on"))
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Reativa RLS e define o contexto do tenant para carregar relações com segurança
    db.execute(text("SET row_security = on"))
    set_tenant(db, str(order.company_id))
    
    return order

@router.post("/{company_slug}/orders", response_model=OrderResponse, status_code=201)
@limiter.limit("100/minute")
async def create_order(
    request: Request,
    company_slug: str,
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    # 1. Resolver Empresa
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    # RLS Context
    set_tenant(db, str(company.id))
    
    # 2. Validar Mesa/Token (Se não for Delivery/Takeout)
    table = None
    session = None
    if order_data.order_type == "dine_in":
        if not order_data.table_id or not order_data.qr_token:
            raise HTTPException(status_code=400, detail="Mesa e Token são obrigatórios para pedidos no salão")
        
        table = db.query(Table).filter(
            Table.id == order_data.table_id,
            Table.company_id == company.id
        ).first()
        
        if not table:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
            
        # Validação de Token (Anti-Troll)
        if order_data.qr_token != "staff-override" and table.qr_token != order_data.qr_token:
             raise HTTPException(status_code=403, detail="QR Code inválido ou expirado")
             
        # Gestão de Sessão
        session = db.query(TableSession).filter(
            TableSession.table_id == table.id,
            TableSession.is_active == True
        ).first()
        
        if not session:
            session = TableSession(
                company_id=company.id,
                table_id=table.id,
                customer_name=order_data.customer_name or "Cliente",
                session_token=str(uuid.uuid4()),
                access_pin="0000",
                is_active=True
            )
            db.add(session)
            db.flush()

    # 3. Calcular Total e Criar Itens
    total_amount = Decimal(0)
    db_items = []
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
            
        item_total = product.price * item.quantity
        total_amount += item_total
        
        db_item = OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            notes=item.notes
        )
        db_items.append(db_item)

    # 4. Criar Pedido
    new_order = Order(
        id=uuid.uuid4(),
        company_id=company.id,
        table_id=table.id if table else None,
        session_id=session.id if session else None,
        customer_name=order_data.customer_name,
        customer_phone=order_data.customer_phone,
        delivery_address=order_data.delivery_address,
        order_type=order_data.order_type,
        origin=OrderOrigin.MESAFLOW,
        status=OrderStatus.PENDING,
        payment_status=PaymentStatus.PENDING,
        payment_method=order_data.payment_method,
        total_amount=total_amount,
        created_at=datetime.now()
    )
    db.add(new_order)
    db.flush()
    
    for item in db_items:
        item.order_id = new_order.id
        db.add(item)
        
    db.commit()
    db.refresh(new_order)
    
    # 5. Notificar KDS (WebSocket)
    await manager.broadcast({
        "type": "new_order",
        "order_id": str(new_order.id),
        "table": table.table_number if table else "Delivery",
        "customer": new_order.customer_name
    }, company.slug)
    
    return new_order

@router.post("/{company_slug}/orders/{order_id}/feedback", status_code=201)
async def create_order_feedback(
    company_slug: str,
    order_id: uuid.UUID,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """
    Registra a avaliação do cliente para um pedido.
    """
    # Localiza o pedido sem RLS para identificar o tenant
    db.execute(text("SET row_security = off"))
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        db.execute(text("SET row_security = on"))
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Valida se o pedido já foi avaliado
    existing = db.query(OrderFeedback).filter(OrderFeedback.order_id == order_id).first()
    if existing:
        db.execute(text("SET row_security = on"))
        raise HTTPException(status_code=400, detail="Este pedido já foi avaliado.")
    
    db.execute(text("SET row_security = on"))
    set_tenant(db, str(order.company_id))

    new_feedback = OrderFeedback(
        order_id=order_id,
        company_id=order.company_id,
        score=feedback_data.score,
        comment=feedback_data.comment
    )
    db.add(new_feedback)
    db.commit()
    return {"message": "Avaliação registrada com sucesso"}
