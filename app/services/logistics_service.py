
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from app.models import Employee, DriverLedger, LedgerType, UserRole, Order, OrderStatus, OrderType
from datetime import date, datetime, time
from decimal import Decimal

class LogisticsService:
    @staticmethod
    def get_dashboard_data(db: Session, company_id: str):
        today = date.today()
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)

        active_drivers = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.role == UserRole.DRIVER,
            Employee.is_active == True
        ).count()

        deliveries_today = db.query(Order).filter(
            Order.company_id == company_id,
            Order.order_type == OrderType.DELIVERY,
            Order.status == OrderStatus.DELIVERED,
            Order.finished_at >= start_of_day
        ).count()

        pending = db.query(Order).filter(
            Order.company_id == company_id,
            Order.order_type == OrderType.DELIVERY,
            Order.status.in_([OrderStatus.READY, OrderStatus.DELIVERING])
        ).count()

        avg_time = db.query(
            func.avg(func.extract('epoch', Order.finished_at - Order.created_at))
        ).filter(
            Order.company_id == company_id,
            Order.status == OrderStatus.DELIVERED,
            Order.finished_at >= start_of_day
        ).scalar() or 0

        total_cash = db.query(func.sum(DriverLedger.amount)).filter(
            DriverLedger.company_id == company_id,
            DriverLedger.type == LedgerType.DEBT,
            DriverLedger.created_at >= start_of_day
        ).scalar() or Decimal(0)

        top_driver = db.query(Employee.name).join(Order, Order.driver_id == Employee.id).filter(
            Order.company_id == company_id,
            Order.status == OrderStatus.DELIVERED,
            Order.finished_at >= start_of_day
        ).group_by(Employee.name).order_by(desc(func.count(Order.id))).first()

        return {
            "active_drivers": active_drivers,
            "deliveries_today": deliveries_today,
            "pending_deliveries": pending,
            "average_delivery_time_minutes": int(avg_time / 60),
            "total_collected_cash": float(total_cash),
            "top_driver": top_driver[0] if top_driver else None
        }

