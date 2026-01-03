from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models import Company, Product, Order, PlanTier

class SaasLimits:
    LIMITS = {
        PlanTier.FREE: {
            "max_products": 15,
            "max_orders_month": 50,
            "allow_kds": True
        },
        PlanTier.PRO: {
            "max_products": 9999,
            "max_orders_month": 9999,
            "allow_kds": True
        }
    }

    @staticmethod
    def check_product_limit(db: Session, company: Company):
        """Verifica se a empresa pode criar mais produtos"""
        if company.plan_tier == PlanTier.PRO:
            return

        current_count = db.query(Product).join(Product.category).filter(
            Product.category.has(company_id=company.id)
        ).count()

        limit = SaasLimits.LIMITS[PlanTier.FREE]["max_products"]
        
        if current_count >= limit:
            raise HTTPException(
                status_code=402, # Payment Required
                detail=f"Limite do Plano Grátis atingido ({limit} produtos). Faça upgrade para o Pro."
            )

    @staticmethod
    def check_order_limit(db: Session, company: Company):
        """Verifica se a empresa pode receber mais pedidos este mês"""
        if company.plan_tier == PlanTier.PRO:
            return

        # Verificar Trial
        if company.trial_ends_at and company.trial_ends_at > datetime.now():
            return # Trial ativo libera tudo

        # Contar pedidos do mês atual
        today = datetime.now()
        start_date = today.replace(day=1, hour=0, minute=0, second=0)
        
        # Lógica para o último dia do mês
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1)

        current_count = db.query(Order).filter(
            Order.company_id == company.id,
            Order.created_at >= start_date,
            Order.created_at < end_date
        ).count()

        limit = SaasLimits.LIMITS[PlanTier.FREE]["max_orders_month"]

        if current_count >= limit:
            raise HTTPException(
                status_code=402,
                detail=f"Limite mensal de pedidos atingido ({limit}). Sua loja está pausada até o upgrade."
            )