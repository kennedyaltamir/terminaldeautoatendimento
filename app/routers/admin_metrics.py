from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, desc, extract, text
from app.database import get_db
from app.models import Company, Order, OrderItem, Product, PaymentStatus, Employee, UserRole
from app.schemas import DashboardMetrics, TopProduct, ChartData, SalesByHour, ProductPerformance, TicketData
from app.routers.auth import get_current_user
from decimal import Decimal
from datetime import date, datetime, time, timedelta
import csv
import io

router = APIRouter()

def require_owner_or_manager(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    if isinstance(current_user, Employee):
        if current_user.role in [UserRole.OWNER, UserRole.MANAGER]:
            return current_user
    raise HTTPException(status_code=403, detail="Acesso negado a dados financeiros")

@router.get("", response_model=DashboardMetrics)
def get_dashboard_metrics(
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: any = Depends(require_owner_or_manager)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id

    if not start_date:
        start_date = date.today() - timedelta(days=6)
    if not end_date:
        end_date = date.today()

    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)

    # 1. KPIs Principais (SQL Otimizado)
    kpi_query = db.query(
        func.sum(Order.total_amount).label('revenue'),
        func.count(Order.id).label('count')
    ).filter(
        Order.company_id == company_id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).first()

    total_revenue = kpi_query.revenue or Decimal(0)
    total_orders = kpi_query.count or 0
    average_ticket = total_revenue / total_orders if total_orders > 0 else Decimal(0)

    # 2. Gráfico de Vendas (Agregação por Dia via SQL)
    # Usa date_trunc para performance em grandes volumes
    chart_query = db.query(
        cast(Order.created_at, Date).label('date'),
        func.sum(Order.total_amount).label('value')
    ).filter(
        Order.company_id == company_id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).group_by(cast(Order.created_at, Date)).order_by(cast(Order.created_at, Date)).all()

    sales_map = {row.date.strftime("%Y-%m-%d"): row.value for row in chart_query}
    chart_data = []
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        chart_data.append(ChartData(
            date=current.strftime("%d/%m"),
            value=sales_map.get(date_str, Decimal(0))
        ))
        current += timedelta(days=1)

    # 3. Vendas por Hora (Heatmap)
    sales_by_hour_query = db.query(
        extract('hour', Order.created_at).label('hour'),
        func.sum(Order.total_amount).label('total'),
        func.count(Order.id).label('count')
    ).filter(
        Order.company_id == company_id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).group_by(extract('hour', Order.created_at)).order_by('hour').all()

    sales_by_hour = [
        SalesByHour(hour=int(row.hour), total=row.total, count=row.count)
        for row in sales_by_hour_query
    ]

    # 4. Top Produtos (Curva ABC)
    product_perf_query = db.query(
        Product.name,
        func.sum(OrderItem.unit_price * OrderItem.quantity).label('revenue'),
        func.sum(OrderItem.quantity).label('quantity')
    ).join(OrderItem).join(Order).filter(
        Order.company_id == company_id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).group_by(Product.name).order_by(desc('revenue')).limit(10).all()

    product_performance = [
        ProductPerformance(name=row.name, revenue=row.revenue, quantity=row.quantity)
        for row in product_perf_query
    ]
    
    top_products = [
        TopProduct(name=p.name, count=p.quantity, revenue=p.revenue) 
        for p in product_performance[:5]
    ]

    # 5. Evolução do Ticket Médio
    ticket_query = db.query(
        cast(Order.created_at, Date).label('date'),
        func.avg(Order.total_amount).label('ticket')
    ).filter(
        Order.company_id == company_id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).group_by(cast(Order.created_at, Date)).order_by(cast(Order.created_at, Date)).all()

    ticket_map = {row.date.strftime("%Y-%m-%d"): row.ticket for row in ticket_query}
    ticket_evolution = []
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        ticket_evolution.append(TicketData(
            date=current.strftime("%d/%m"),
            ticket=ticket_map.get(date_str, Decimal(0))
        ))
        current += timedelta(days=1)

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_ticket": average_ticket,
        "top_products": top_products,
        "sales_chart": chart_data,
        "sales_by_hour": sales_by_hour,
        "product_performance": product_performance,
        "ticket_evolution": ticket_evolution
    }

@router.get("/export", response_class=StreamingResponse)
def export_sales_report(
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: any = Depends(require_owner_or_manager)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id

    if not start_date: start_date = date.today() - timedelta(days=30)
    if not end_date: end_date = date.today()

    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)

    orders = db.query(Order).filter(
        Order.company_id == company_id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).order_by(Order.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["ID Pedido", "Data", "Hora", "Cliente", "Mesa", "Tipo", "Pagamento", "Total (R$)", "Status"])

    for order in orders:
        writer.writerow([
            str(order.id)[:8],
            order.created_at.strftime("%d/%m/%Y"),
            order.created_at.strftime("%H:%M"),
            order.customer_name or "Anônimo",
            order.table.table_number if order.table else "Delivery",
            "Entrega" if order.order_type == "delivery" else "Mesa",
            order.payment_method.upper(),
            f"{order.total_amount:.2f}".replace(".", ","),
            order.status.upper()
        ])

    output.seek(0)
    
    filename = f"vendas_{start_date}_{end_date}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )