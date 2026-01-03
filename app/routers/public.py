from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import func
from app.database import get_db
from app.models import Company, Category, Table, Product, Order, OrderItem, OrderStatus, Option, OrderItemOption, OptionGroup, PaymentMethod, OrderType, ServiceRequest, ServiceType, CustomerWallet, TableSession, PaymentStatus
from app.schemas import MenuResponse, OrderCreate, OrderResponse, ServiceRequestCreate, ServiceRequestResponse, WalletResponse, CheckTableRequest, CheckTableResponse, TableSessionResponse, JoinTableRequest
from app.services.payment_service import PaymentService
from app.services.stock_service import StockService
from app.websockets import manager
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import uuid
import random

router = APIRouter()
payment_service = PaymentService()
stock_service = StockService()

def is_restaurant_open(company: Company) -> bool:
    if not company.opens_at or not company.closes_at:
        return True
    now = datetime.now().time()
    if company.opens_at < company.closes_at:
        return company.opens_at <= now <= company.closes_at
    return now >= company.opens_at or now <= company.closes_at

@router.get("/{company_slug}/menu", response_model=MenuResponse)
def get_menu(company_slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    # Buscar todas as categorias
    all_categories = (
        db.query(Category)
        .options(
            selectinload(Category.products)
            .selectinload(Product.option_groups)
            .selectinload(OptionGroup.options),
            selectinload(Category.products).selectinload(Product.recommendations)
        )
        .filter(Category.company_id == company.id)
        .order_by(Category.order_index)
        .all()
    )

    # --- FILTRAGEM POR HORÁRIO E DIA ---
    now = datetime.now()
    current_time = now.time()
    current_weekday = now.weekday() # 0=Segunda, 6=Domingo (Python padrão)
    # Ajuste: No frontend/banco geralmente usamos 0=Domingo. Vamos padronizar:
    # Python: 0=Mon, 6=Sun.
    # Nosso padrão (JS): 0=Sun, 1=Mon.
    # Conversão: (weekday + 1) % 7
    js_weekday = (current_weekday + 1) % 7

    visible_categories = []
    for cat in all_categories:
        # 1. Verificar Dias da Semana
        if cat.availability_days is not None:
            # Se a lista não estiver vazia e o dia atual não estiver nela, pular
            if len(cat.availability_days) > 0 and js_weekday not in cat.availability_days:
                continue
        
        # 2. Verificar Horário
        if cat.start_time and cat.end_time:
            start = cat.start_time
            end = cat.end_time
            is_active = False
            
            if start < end:
                is_active = start <= current_time <= end
            else: # Passa da meia-noite (ex: 18:00 as 02:00)
                is_active = current_time >= start or current_time <= end
            
            if not is_active:
                continue

        visible_categories.append(cat)

    return {
        "company": company,
        "categories": visible_categories
    }

@router.get("/{company_slug}/wallet/{phone}", response_model=WalletResponse)
def get_customer_wallet(company_slug: str, phone: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    clean_phone = "".join(filter(str.isdigit, phone))
    
    wallet = db.query(CustomerWallet).filter(
        CustomerWallet.company_id == company.id,
        CustomerWallet.customer_phone == clean_phone
    ).first()
    
    return {
        "balance": wallet.balance if wallet else Decimal(0),
        "loyalty_percentage": company.loyalty_percentage or Decimal(0)
    }

@router.post("/{company_slug}/check-table", response_model=CheckTableResponse)
def check_table_status(
    company_slug: str,
    data: CheckTableRequest,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company: raise HTTPException(404, "Empresa não encontrada")

    table = db.query(Table).filter(Table.id == data.table_id, Table.company_id == company.id).first()
    if not table or table.qr_token != data.qr_token:
        raise HTTPException(403, "QR Code inválido")

    active_session = db.query(TableSession).filter(
        TableSession.table_id == table.id,
        TableSession.is_active == True
    ).first()

    if not active_session:
        return {"status": "free"}

    if data.session_token and data.session_token == active_session.session_token:
        return {
            "status": "active", 
            "customer_name": active_session.customer_name,
            "session_token": active_session.session_token
        }
    
    return {
        "status": "blocked",
        "customer_name": active_session.customer_name,
        "requires_pin": True
    }

@router.post("/{company_slug}/join-table", response_model=TableSessionResponse)
def join_table(
    company_slug: str,
    data: JoinTableRequest,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company: raise HTTPException(404, "Empresa não encontrada")

    table = db.query(Table).filter(Table.id == data.table_id, Table.company_id == company.id).first()
    if not table or table.qr_token != data.qr_token:
        raise HTTPException(403, "QR Code inválido")

    active_session = db.query(TableSession).filter(
        TableSession.table_id == table.id,
        TableSession.is_active == True
    ).first()

    if not active_session:
        pin = f"{random.randint(1000, 9999)}"
        new_session = TableSession(
            company_id=company.id,
            table_id=table.id,
            customer_name=data.customer_name,
            session_token=str(uuid.uuid4()),
            access_pin=pin
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    if data.pin == active_session.access_pin:
        return active_session
    
    raise HTTPException(403, "PIN incorreto")

@router.get("/{company_slug}/session/{session_token}", response_model=TableSessionResponse)
def get_table_session(
    company_slug: str,
    session_token: str,
    db: Session = Depends(get_db)
):
    session = db.query(TableSession).filter(
        TableSession.session_token == session_token,
        TableSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(404, "Sessão não encontrada ou encerrada")

    orders = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options)
    ).filter(Order.session_id == session.id).order_by(Order.created_at.desc()).all()

    total_spent = sum(o.total_amount for o in orders)

    return {
        "id": session.id,
        "customer_name": session.customer_name,
        "is_active": session.is_active,
        "created_at": session.created_at,
        "orders": orders,
        "total_spent": total_spent,
        "access_pin": session.access_pin
    }

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_status(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(Order).options(
        selectinload(Order.table),
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options)
    ).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    return order

@router.post("/{company_slug}/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    company_slug: str, 
    order_data: OrderCreate, 
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    if not is_restaurant_open(company):
        raise HTTPException(status_code=403, detail="Restaurante fechado")

    table = None
    session = None

    if order_data.order_type == "dine_in":
        if not order_data.table_id or not order_data.qr_token:
             raise HTTPException(status_code=400, detail="Mesa e Token obrigatórios.")
        table = db.query(Table).filter(Table.id == order_data.table_id, Table.company_id == company.id).first()
        if not table or table.qr_token != order_data.qr_token:
            raise HTTPException(status_code=403, detail="Mesa inválida")
        
        session = db.query(TableSession).filter(
            TableSession.table_id == table.id,
            TableSession.is_active == True
        ).first()

        if not session:
            raise HTTPException(400, "Faça o check-in na mesa primeiro.")

    elif order_data.order_type == "delivery":
        if not order_data.delivery_address or not order_data.customer_phone:
            raise HTTPException(status_code=400, detail="Dados de entrega incompletos.")

    subtotal = Decimal(0)
    db_items = []

    for item in order_data.items:
        product = db.query(Product).join(Category).filter(Product.id == item.product_id, Category.company_id == company.id).with_for_update().first()
        if not product or not product.is_available:
            raise HTTPException(status_code=400, detail=f"Produto indisponível")
        
        if product.track_stock:
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Estoque insuficiente: {product.name}")
            product.stock_quantity -= item.quantity

        item_price = product.price
        selected_options_db = []
        if item.selected_options:
            options = db.query(Option).filter(Option.id.in_(item.selected_options)).all()
            for opt in options:
                item_price += opt.price
                selected_options_db.append(OrderItemOption(option_id=opt.id, name=opt.name, price=opt.price))

        subtotal += item_price * item.quantity
        db_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            notes=item.notes,
            selected_options=selected_options_db
        ))

    discount_amount = Decimal(0)
    clean_phone = "".join(filter(str.isdigit, order_data.customer_phone)) if order_data.customer_phone else None

    if order_data.use_balance and clean_phone:
        wallet = db.query(CustomerWallet).filter(
            CustomerWallet.company_id == company.id,
            CustomerWallet.customer_phone == clean_phone
        ).with_for_update().first()
        
        if wallet and wallet.balance > 0:
            discount_amount = min(wallet.balance, subtotal)
            wallet.balance -= discount_amount
            db.add(wallet)

    total_amount = subtotal - discount_amount

    cashback_earned = Decimal(0)
    if company.loyalty_percentage > 0 and total_amount > 0:
        cashback_earned = total_amount * (company.loyalty_percentage / Decimal(100))

    new_order = Order(
        company_id=company.id, 
        table_id=table.id if table else None, 
        session_id=session.id if session else None,
        order_type=order_data.order_type,
        customer_name=order_data.customer_name,
        customer_phone=clean_phone,
        delivery_address=order_data.delivery_address,
        
        subtotal=subtotal,
        discount_amount=discount_amount,
        total_amount=total_amount,
        cashback_earned=cashback_earned,
        
        status=OrderStatus.PENDING,
        payment_method=order_data.payment_method
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for db_item in db_items:
        db_item.order_id = new_order.id
    db.add_all(db_items)
    
    stock_service.deduct_stock_for_order(db, db_items)

    db.commit()

    if order_data.payment_method == "online" and total_amount > 0: 
        try:
            payment_info = await payment_service.create_pix_payment(new_order, company)
            new_order.mp_payment_id = payment_info["id"]
            new_order.mp_qr_code = payment_info["qr_code"]
            new_order.mp_qr_code_base64 = payment_info["qr_code_base64"]
            db.commit()
        except Exception as e:
            print(f"Erro Pix: {e}")
    elif total_amount == 0:
        new_order.payment_status = PaymentStatus.PAID
        new_order.status = OrderStatus.ACCEPTED
        db.commit()

    await manager.broadcast({
        "type": "new_order",
        "order_id": str(new_order.id),
        "table": table.table_number if table else "DELIVERY",
        "order_type": new_order.order_type
    }, company_slug)

    return db.query(Order).options(
        selectinload(Order.table),
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options)
    ).filter(Order.id == new_order.id).first()

@router.post("/{company_slug}/service", response_model=ServiceRequestResponse, status_code=201)
async def request_service(
    company_slug: str,
    request_data: ServiceRequestCreate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    table = db.query(Table).filter(
        Table.id == request_data.table_id,
        Table.company_id == company.id
    ).first()

    if not table or table.qr_token != request_data.qr_token:
        raise HTTPException(status_code=403, detail="Mesa inválida")

    existing = db.query(ServiceRequest).filter(
        ServiceRequest.table_id == table.id,
        ServiceRequest.status == "pending"
    ).first()

    if existing:
        existing.service_type = request_data.service_type
        existing.notes = request_data.notes
        existing.created_at = func.now()
        db.commit()
        db.refresh(existing)
        
        await manager.broadcast({
            "type": "waiter_call",
            "id": existing.id,
            "table": table.table_number,
            "service_type": existing.service_type,
            "notes": existing.notes
        }, company_slug)
        
        return existing

    new_request = ServiceRequest(
        company_id=company.id,
        table_id=table.id,
        service_type=request_data.service_type,
        notes=request_data.notes,
        status="pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    await manager.broadcast({
        "type": "waiter_call",
        "id": new_request.id,
        "table": table.table_number,
        "service_type": new_request.service_type,
        "notes": new_request.notes
    }, company_slug)

    return new_request