# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Company, Order, OrderItem, ProductRecipe, Ingredient, OrderStatus, PaymentStatus
from decimal import Decimal
from datetime import date, datetime, time

class FranchiseService:
    @staticmethod
    def get_network_summary(db: Session, owner_email: str):
        companies = db.query(Company).filter(Company.owner_email == owner_email).all()
        today = date.today()
        start_dt = datetime.combine(today, time.min)
        end_dt = datetime.combine(today, time.max)
        
        stores_data = []
        for company in companies:
            stats = FranchiseService._get_store_day_stats(db, company, start_dt, end_dt)
            stores_data.append(stats)
            
        return {
            "total_revenue": sum(s["revenue"] for s in stores_data),
            "total_profit": sum(s["profit"] for s in stores_data),
            "total_orders": sum(s["orders_count"] for s in stores_data),
            "stores": stores_data
        }

    @staticmethod
    def _get_store_day_stats(db, company, start_dt, end_dt):
        metrics = db.query(
            func.sum(Order.total_amount).label('rev'),
            func.sum(Order.service_fee).label('fees'),
            func.count(Order.id).label('cnt')
        ).filter(
            Order.company_id == company.id,
            Order.status != OrderStatus.CANCELED,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_dt,
            Order.created_at <= end_dt
        ).first()

        rev = metrics.rev or Decimal(0)
        orders_count = int(metrics.cnt or 0)
        
        cmv = db.query(
            func.sum(OrderItem.quantity * ProductRecipe.quantity_required * Ingredient.cost_per_unit)
        ).join(Order, Order.id == OrderItem.order_id)\
         .join(ProductRecipe, ProductRecipe.product_id == OrderItem.product_id)\
         .join(Ingredient, Ingredient.id == ProductRecipe.ingredient_id)\
         .filter(Order.company_id == company.id, Order.created_at >= start_dt).scalar() or 0
        
        profit = float(rev) - float(cmv) - float(metrics.fees or 0)
        margin = (profit / float(rev) * 100) if rev > 0 else 0
        
        return {
            "id": str(company.id),
            "name": company.name,
            "slug": company.slug,
            "revenue": float(rev),
            "cmv": float(cmv),
            "fees": float(metrics.fees or 0),
            "profit": profit,
            "margin_percent": margin,
            "orders_count": orders_count
        }

