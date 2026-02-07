# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54

from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, desc, extract
from app.models import Order, OrderItem, Product, PaymentStatus
from app.schemas import ChartData, SalesByHour, ProductPerformance, TicketData, TopProduct
from decimal import Decimal
from datetime import date, datetime, time, timedelta

class MetricsService:
    @staticmethod
    def get_aggregate_metrics(db: Session, company_id: str, start_date: date, end_date: date):
        start_dt = datetime.combine(start_date, time.min)
        end_dt = datetime.combine(end_date, time.max)

        # KPIs
        kpi = db.query(
            func.sum(Order.total_amount).label('revenue'),
            func.count(Order.id).label('count')
        ).filter(
            Order.company_id == company_id,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_dt,
            Order.created_at <= end_dt
        ).first()

        rev = kpi.revenue or Decimal(0)
        count = kpi.count or 0
        avg_ticket = rev / count if count > 0 else Decimal(0)

        return {
            "total_revenue": float(rev),
            "total_orders": count,
            "average_ticket": float(avg_ticket),
            "sales_chart": MetricsService._get_sales_chart(db, company_id, start_date, end_date),
            "sales_by_hour": MetricsService._get_sales_by_hour(db, company_id, start_dt, end_dt),
            "product_performance": MetricsService._get_product_performance(db, company_id, start_dt, end_dt)
        }

    @staticmethod
    def _get_sales_chart(db, company_id, start_date, end_date):
        query = db.query(
            cast(Order.created_at, Date).label('date'),
            func.sum(Order.total_amount).label('value')
        ).filter(
            Order.company_id == company_id,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= datetime.combine(start_date, time.min),
            Order.created_at <= datetime.combine(end_date, time.max)
        ).group_by(cast(Order.created_at, Date)).all()
        
        sales_map = {row.date.strftime("%Y-%m-%d"): row.value for row in query}
        chart = []
        curr = start_date
        while curr <= end_date:
            d_str = curr.strftime("%Y-%m-%d")
            chart.append({"date": curr.strftime("%d/%m"), "value": float(sales_map.get(d_str, 0))})
            curr += timedelta(days=1)
        return chart

    @staticmethod
    def _get_sales_by_hour(db, company_id, start_dt, end_dt):
        query = db.query(
            extract('hour', Order.created_at).label('hour'),
            func.sum(Order.total_amount).label('total'),
            func.count(Order.id).label('count')
        ).filter(
            Order.company_id == company_id,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_dt,
            Order.created_at <= end_dt
        ).group_by(extract('hour', Order.created_at)).all()
        return [{"hour": int(r.hour), "total": float(r.total), "count": r.count} for r in query]

    @staticmethod
    def _get_product_performance(db, company_id, start_dt, end_dt):
        query = db.query(
            Product.name,
            func.sum(OrderItem.unit_price * OrderItem.quantity).label('revenue'),
            func.sum(OrderItem.quantity).label('quantity')
        ).join(OrderItem).join(Order).filter(
            Order.company_id == company_id,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_dt,
            Order.created_at <= end_dt
        ).group_by(Product.name).order_by(desc('revenue')).limit(10).all()
        return [{"name": r.name, "revenue": float(r.revenue), "quantity": int(r.quantity)} for r in query]

