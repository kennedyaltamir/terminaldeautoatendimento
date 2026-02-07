# DOMAIN: BACKEND / ORDERS
# LAST_MODIFIED: 2026-01-27 23:30:00
# DESCRIPTION: Router de Pedidos Público - Hardened para evitar erros de validação.
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import uuid
import re
from app.database import get_db, set_tenant
from app.models import Company, Order, OrderItem, Product, OrderStatus, PaymentStatus
from app.schemas.orders import OrderCreate, OrderResponse
from decimal import Decimal

router = APIRouter()

@router.post("/{company_slug}/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    company_slug: str,
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    set_tenant(db, str(company.id))

    # 🛡️ Sanitização de Telefone
    clean_phone = re.sub(r"\D", "", order_data.customer_phone or "")
    if clean_phone and not clean_phone.startswith("55"):
        clean_phone = f"55{clean_phone}"

    try:
        new_order = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            table_id=order_data.table_id,
            customer_name=order_data.customer_name,
            customer_phone=clean_phone,
            delivery_address=order_data.delivery_address,
            order_type=order_data.order_type,
            origin=order_data.origin,
            pickup_note=order_data.pickup_note,
            payment_method=order_data.payment_method,
            status=OrderStatus.PENDING.value,
            payment_status=PaymentStatus.PENDING.value,
            total_amount=Decimal("0.00"),
            device_fingerprint="web_client_forensic"
        )
        db.add(new_order)
        
        total = Decimal("0.00")
        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                price = Decimal(str(product.price))
                total += price * item.quantity
                db.add(OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=price
                ))
        
        new_order.total_amount = total
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
