# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 14:10:00
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, selectinload
from app.database import get_db, set_tenant
from app.models import Company, Category, Product, OptionGroup, CustomerWallet, Order, OrderStatus
from app.schemas import MenuResponse, WalletResponse
from app.core.limiter import limiter
from app.core.cache import cache_response
from datetime import datetime
from decimal import Decimal

router = APIRouter()

@router.get("/resolve-domain")
def resolve_domain(host: str, db: Session = Depends(get_db)):
    # Remove porta e normaliza
    clean_host = host.split(":")[0].lower()
    
    # RESILIÊNCIA L6: Suporte explícito para desenvolvimento local
    if clean_host in ["localhost", "127.0.0.1", "0.0.0.0"]:
        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        if company:
            return {"slug": company.slug, "valid": True, "env": "dev_bypass"}

    company = db.query(Company).filter(Company.custom_domain == clean_host).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Domínio '{clean_host}' não mapeado.")
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
            selectinload(Category.products).selectinload(Product.option_groups).selectinload(OptionGroup.options),
            selectinload(Category.products).selectinload(Product.recommendations)
        )
        .filter(Category.company_id == company.id)
        .order_by(Category.order_index).all()
    )
    return {"company": company, "categories": all_categories}

@router.get("/{company_slug}/monitor")
def get_public_monitor_orders(company_slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company: raise HTTPException(status_code=404)
    set_tenant(db, str(company.id))
    orders = db.query(Order).filter(
        Order.company_id == company.id,
        Order.status.in_(["pending", "accepted", "preparing", "ready"])
    ).order_by(Order.created_at.desc()).limit(20).all()
    return [{"id": str(o.id), "display_id": str(o.id)[-4:].upper(), "status": o.status, "customer_name": o.customer_name} for o in orders]
