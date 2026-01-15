# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 13:35:00
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, selectinload
from app.database import get_db, set_tenant
from app.models import Company, Category, Product, OptionGroup, CustomerWallet, Order, OrderStatus
from app.schemas import MenuResponse, WalletResponse
from app.core.limiter import limiter
from app.core.cache import cache_response
from datetime import datetime
from decimal import Decimal
from typing import List

router = APIRouter()

@router.get("/resolve-domain")
def resolve_domain(host: str, db: Session = Depends(get_db)):
    clean_host = host.split(":")[0]
    
    # RESILIÊNCIA L6: Bypass para ambiente de desenvolvimento
    if clean_host in ["localhost", "127.0.0.1"]:
        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        if company:
            return {"slug": company.slug, "valid": True, "env": "development"}

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
    
    set_tenant(db, str(company.id))
    
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
    js_weekday = (now.weekday() + 1) % 7
    
    visible_categories = []
    for cat in all_categories:
        if cat.availability_days is not None and len(cat.availability_days) > 0:
            if js_weekday not in cat.availability_days:
                continue
        if cat.start_time and cat.end_time:
            if not (cat.start_time <= current_time <= cat.end_time):
                continue
        visible_categories.append(cat)
        
    return {"company": company, "categories": visible_categories}

@router.get("/{company_slug}/monitor")
def get_public_monitor_orders(company_slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    set_tenant(db, str(company.id))
    
    orders = db.query(Order).filter(
        Order.company_id == company.id,
        Order.status.in_([
            OrderStatus.PENDING.value, 
            OrderStatus.ACCEPTED.value, 
            OrderStatus.PREPARING.value, 
            OrderStatus.READY.value
        ])
    ).order_by(Order.created_at.desc()).limit(20).all()
    
    return [
        {
            "id": str(o.id),
            "display_id": str(o.id)[-4:].upper(),
            "status": o.status,
            "customer_name": o.customer_name
        } for o in orders
    ]

@router.get("/{company_slug}/wallet/{phone}", response_model=WalletResponse)
@limiter.limit("10/minute")
def get_customer_wallet(request: Request, company_slug: str, phone: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    set_tenant(db, str(company.id))
    clean_phone = "".join(filter(str.isdigit, phone))
    
    wallet = db.query(CustomerWallet).filter(
        CustomerWallet.company_id == company.id,
        CustomerWallet.customer_phone == clean_phone
    ).first()
    
    return {
        "balance": wallet.balance if wallet else Decimal(0),
        "loyalty_percentage": company.loyalty_percentage or Decimal(0)
    }

