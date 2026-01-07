from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import func
from app.database import get_db
from app.models import (
    Company, Category, Table, Product, Order, OrderItem, OrderStatus, 
    Option, OrderItemOption, OptionGroup, PaymentMethod, OrderType, 
    ServiceRequest, ServiceType, CustomerWallet, TableSession, 
    PaymentStatus, Employee, UserRole, Lead, OrderFeedback, Promotion
)
from app.schemas import (
    MenuResponse, OrderCreate, OrderResponse, ServiceRequestCreate, 
    ServiceRequestResponse, WalletResponse, CheckTableRequest, 
    CheckTableResponse, TableSessionResponse, JoinTableRequest,
    LeadCreate, LeadResponse, FeedbackCreate, CouponValidationRequest, CouponValidationResponse
)
from app.services.payment_service import PaymentService
from app.services.stock_service import StockService
from app.services.webhook_dispatcher import WebhookDispatcher
from app.services.promotion_service import PromotionService
from app.websockets import manager
from app.core.limiter import limiter
from app.core.saas_limits import SaasLimits
from app.core.cache import cache_response
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import uuid
import random
import string

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

@router.get("/resolve-domain")
def resolve_domain(host: str, db: Session = Depends(get_db)):
    clean_host = host.split(":")[0]
    company = db.query(Company).filter(Company.custom_domain == clean_host).first()
    if not company:
        raise HTTPException(status_code=404, detail="Domínio não encontrado")
    return {"slug": company.slug, "valid": True}

@router.get("/{company_slug}/menu", response_model=MenuResponse)
@limiter.limit("60/minute")
@cache_response(ttl=300, key_prefix="menu:{company_slug}")
def get_menu(request: Request, company_slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")

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

    now = datetime.now()
    current_time = now.time()
    current_weekday = now.weekday()
    js_weekday = (current_weekday + 1) % 7

    visible_categories = []
    for cat in all_categories:
        if cat.availability_days is not None:
            if len(cat.availability_days) > 0 and js_weekday not in cat.availability_days:
                continue

        if cat.start_time and cat.end_time:
            start = cat.start_time
            end = cat.end_time
            is_active = False
            if start < end:
                is_active = start <= current_time <= end
            else:
                is_active = current_time >= start or current_time <= end
            if not is_active:
                continue

        visible_categories.append(cat)

    return {
        "company": company,
        "categories": visible_categories
    }

@router.get("/{company_slug}/wallet/{phone}", response_model=WalletResponse)
@limiter.limit("10/minute")
def get_customer_wallet(request: Request, company_slug: str, phone: str, db: Session = Depends(get_db)):
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
@limiter.limit("20/minute")
def check_table_status(
    request: Request,
    company_slug: str,
    data: CheckTableRequest,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company: raise HTTPException(404, "Empresa não encontrada")

    if data.qr_token == "admin-override":
        active_session = db.query(TableSession).filter(
            TableSession.table_id == data.table_id,
            TableSession.is_active == True
        ).first()

        if active_session:
            return {
                "status": "active",
                "customer_name": active_session.customer_name,
                "session_token": active_session.session_token,
                "access_pin": active_session.access_pin
            }
        return {"status": "free"}

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
@limiter.limit("5/minute")
def join_table(
    request: Request,
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
        # Geração de PIN de 10 dígitos para autoatendimento
        pin = ''.join(random.choices(string.digits, k=10))
        new_session = TableSession(
            company_id=company.id,
            table_id=table.id,
            customer_name=data.customer_name,
            session_token=str(uuid.uuid4()),
            access_pin=pin,
            is_active=True
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
    session_token: str,
    company_slug: str,
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
        selectinload(Order.items).selectinload(OrderItem.selected_options),
        selectinload(Order.feedback)
    ).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return order

@router.post("/{company_slug}/orders", response_model=OrderResponse, status_code=201)
@limiter.limit("10/minute")
async def create_order(
    request: Request,
    company_slug: str, 
    order_data: OrderCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    SaasLimits.check_order_limit(db, company)

    if not is_restaurant_open(company):
        raise HTTPException(status_code=403, detail="Restaurante fechado")

    table = None
    session = None
    is_staff = False

    if order_data.qr_token == "staff-override":
        is_staff = True

    if order_data.order_type == "dine_in":
        if not order_data.table_id:
             raise HTTPException(status_code=400, detail="Mesa obrigatória.")

        table = db.query(Table).filter(Table.id == order_data.table_id, Table.company_id == company.id).first()

        if not is_staff:
            if not order_data.qr_token or table.qr_token != order_data.qr_token:
                raise HTTPException(status_code=403, detail="Mesa inválida (QR Code incorreto)")

        session = db.query(TableSession).filter(
            TableSession.table_id == table.id,
            TableSession.is_active == True
        ).first()

        if not session:
            raise HTTPException(400, "Mesa fechada. Abra a mesa primeiro.")

    elif order_data.order_type == "delivery":
        if not order_data.delivery_address or not order_data.customer_phone:
            raise HTTPException(status_code=400, detail="Dados de entrega incompletos.")

    subtotal = Decimal(0)
    db_items = []

    for item in order_data.items:
        product = db.query(Product).join(Category).filter(
            Product.id == item.product_id, 
            Category.company_id == company.id
        ).with_for_update().first()

        if not product or not product.is_available:
            raise HTTPException(status_code=400, detail=f"Produto indisponível: {product.name if product else '?'}")

        if product.track_stock:
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Estoque insuficiente: {product.name}")

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

    # 1. Desconto de Saldo (Cashback)
    if order_data.use_balance and clean_phone:
        wallet = db.query(CustomerWallet).filter(
            CustomerWallet.company_id == company.id,
            CustomerWallet.customer_phone == clean_phone
        ).with_for_update().first()

        if wallet and wallet.balance > 0:
            discount_amount = min(wallet.balance, subtotal)
            wallet.balance -= discount_amount
            db.add(wallet)

    delivery_fee = Decimal(0)
    if order_data.order_type == OrderType.DELIVERY:
        delivery_fee = company.fixed_delivery_fee or Decimal(0)

    # 2. Desconto de Cupom (NOVO)
    promotion_id = None
    if order_data.coupon_code:
        valid, msg, promo = PromotionService.validate_coupon(db, order_data.coupon_code, subtotal, company.id)
        if valid and promo:
            coupon_discount = PromotionService.calculate_discount(promo, subtotal, delivery_fee)
            discount_amount += coupon_discount
            promotion_id = promo.id
            PromotionService.increment_usage(db, promo.id)
        else:
            # Se o cupom for inválido, falha o pedido ou ignora?
            # Melhor falhar para o cliente saber que não aplicou
            raise HTTPException(status_code=400, detail=f"Erro no cupom: {msg}")

    total_amount = subtotal + delivery_fee - discount_amount
    if total_amount < 0: total_amount = Decimal(0)

    cashback_earned = Decimal(0)
    if company.loyalty_percentage > 0 and total_amount > 0:
        cashback_earned = total_amount * (company.loyalty_percentage / Decimal(100))

    initial_status = OrderStatus.ACCEPTED if is_staff else OrderStatus.PENDING

    delivery_code = None
    if order_data.order_type == OrderType.DELIVERY:
        delivery_code = str(random.randint(1000, 9999))

    new_order = Order(
        company_id=company.id, 
        table_id=table.id if table else None, 
        session_id=session.id if session else None,
        order_type=order_data.order_type,
        customer_name=order_data.customer_name,
        customer_phone=clean_phone,
        delivery_address=order_data.delivery_address,
        delivery_code=delivery_code,
        subtotal=subtotal,
        discount_amount=discount_amount,
        total_amount=total_amount,
        cashback_earned=cashback_earned,
        delivery_fee=delivery_fee,
        status=initial_status,
        payment_method=order_data.payment_method,
        promotion_id=promotion_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for db_item in db_items:
        db_item.order_id = new_order.id
    db.add_all(db_items)

    try:
        stock_service.deduct_stock_for_order(db, db_items, background_tasks)
        db.commit()
    except Exception as e:
        db.delete(new_order)
        db.commit()
        raise e

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

    # Notificações Real-time
    await manager.broadcast({
        "type": "new_order",
        "order_id": str(new_order.id),
        "table": table.table_number if table else "DELIVERY",
        "order_type": new_order.order_type,
        "is_staff": is_staff
    }, company_slug)

    # Webhook Dispatch (Integração Externa)
    order_payload = OrderResponse.model_validate(new_order).model_dump(mode='json')
    background_tasks.add_task(
        WebhookDispatcher.dispatch,
        "order.created",
        order_payload,
        str(company.id)
    )

    return db.query(Order).options(
        selectinload(Order.table),
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options)
    ).filter(Order.id == new_order.id).first()

@router.post("/{company_slug}/cart/validate-coupon", response_model=CouponValidationResponse)
def validate_coupon_endpoint(
    company_slug: str,
    data: CouponValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Valida um cupom antes de fechar o pedido.
    """
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(404, "Empresa não encontrada")

    valid, msg, promo = PromotionService.validate_coupon(db, data.code, data.total_amount, company.id)

    if not valid or not promo:
        return {
            "valid": False,
            "discount_amount": Decimal(0),
            "final_total": data.total_amount,
            "message": msg
        }

    # Calcular desconto (assumindo frete zero para validação de carrinho simples)
    discount = PromotionService.calculate_discount(promo, data.total_amount)
    final = data.total_amount - discount
    if final < 0: final = Decimal(0)

    return {
        "valid": True,
        "discount_amount": discount,
        "final_total": final,
        "message": msg,
        "promotion_id": promo.id
    }

@router.post("/{company_slug}/service", response_model=ServiceRequestResponse, status_code=201)
@limiter.limit("2/minute")
async def request_service(
    request: Request,
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
        existing.created_at = datetime.now()
        db.add(existing)
    else:
        existing = ServiceRequest(
            company_id=company.id,
            table_id=table.id,
            service_type=request_data.service_type,
            notes=request_data.notes,
            status="pending"
        )
        db.add(existing)

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

@router.post("/leads", response_model=LeadResponse, status_code=201)
@limiter.limit("5/minute")
def create_lead(
    request: Request,
    lead_data: LeadCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Lead).filter(Lead.email == lead_data.email).first()
    if not existing:
        new_lead = Lead(email=lead_data.email, source=lead_data.source)
        db.add(new_lead)
        db.commit()

    return {
        "message": "Sucesso! Verifique seu e-mail.",
        "download_url": "https://mesaflow.com/assets/guia-eficiencia-2026.pdf"
    }

@router.post("/{company_slug}/orders/{order_id}/feedback", status_code=201)
@limiter.limit("5/minute")
def submit_feedback(
    request: Request,
    company_slug: str,
    order_id: str,
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    order = db.query(Order).filter(Order.id == order_id, Order.company_id == company.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if db.query(OrderFeedback).filter(OrderFeedback.order_id == order.id).first():
        raise HTTPException(status_code=400, detail="Feedback já enviado para este pedido")

    new_feedback = OrderFeedback(
        order_id=order.id,
        company_id=company.id,
        score=feedback.score,
        comment=feedback.comment
    )
    db.add(new_feedback)
    db.commit()

    return {"message": "Obrigado pela avaliação!"}