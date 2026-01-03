from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, desc
from app.database import get_db
from app.models import Company, Order, OrderItem, Product, PaymentStatus
from app.schemas import DashboardMetrics, TopProduct, ChartData, SalesByHour, ProductPerformance, TicketData
from app.routers.auth import get_current_user
from decimal import Decimal
from datetime import date, datetime, time, timedelta

router = APIRouter()

@router.get("", response_model=DashboardMetrics)
def get_dashboard_metrics(
    start_date: date = Query(None),
    end_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    # Se não passar data, assume últimos 7 dias para o gráfico
    if not start_date:
        start_date = date.today() - timedelta(days=6)
    if not end_date:
        end_date = date.today()

    # Base query para pedidos pagos
    base_query = db.query(Order).filter(
        Order.company_id == current_user.id,
        Order.payment_status == PaymentStatus.PAID
    )

    # Filtros de data
    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)
    
    filtered_query = base_query.filter(
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    )

    # 1. Métricas Totais
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.id.in_(filtered_query.with_entities(Order.id))
    ).scalar() or Decimal(0)

    total_orders = filtered_query.count()
    average_ticket = total_revenue / total_orders if total_orders > 0 else Decimal(0)

    # 2. Top Produtos (Quantidade)
    top_products_query = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label("total_qty")
    ).join(OrderItem).join(Order).filter(
        Order.id.in_(filtered_query.with_entities(Order.id))
    ).group_by(Product.name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()

    top_products = [TopProduct(name=row[0], count=int(row[1])) for row in top_products_query]

    # 3. Dados do Gráfico de Vendas (Agrupado por Dia)
    chart_query = db.query(
        cast(Order.created_at, Date).label('date'),
        func.sum(Order.total_amount).label('value')
    ).filter(
        Order.company_id == current_user.id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).group_by(cast(Order.created_at, Date)).order_by(cast(Order.created_at, Date)).all()

    sales_map = {row[0].strftime("%Y-%m-%d"): row[1] for row in chart_query}
    chart_data = []
    
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        chart_data.append(ChartData(
            date=current.strftime("%d/%m"),
            value=sales_map.get(date_str, Decimal(0))
        ))
        current += timedelta(days=1)

    # --- NOVAS MÉTRICAS AVANÇADAS ---

    # 4. Vendas por Hora (Heatmap)
    sales_by_hour_query = db.query(
        func.extract('hour', Order.created_at).label('hour'),
        func.sum(Order.total_amount).label('total'),
        func.count(Order.id).label('count')
    ).filter(
        Order.company_id == current_user.id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).group_by(func.extract('hour', Order.created_at)).order_by('hour').all()

    sales_by_hour = [
        SalesByHour(hour=int(row.hour), total=row.total, count=row.count)
        for row in sales_by_hour_query
    ]

    # 5. Curva ABC (Performance de Produto por Receita)
    product_perf_query = db.query(
        Product.name,
        func.sum(OrderItem.unit_price * OrderItem.quantity).label('revenue'),
        func.sum(OrderItem.quantity).label('quantity')
    ).join(OrderItem).join(Order).filter(
        Order.id.in_(filtered_query.with_entities(Order.id))
    ).group_by(Product.name).order_by(desc('revenue')).limit(10).all()

    product_performance = [
        ProductPerformance(name=row.name, revenue=row.revenue, quantity=row.quantity)
        for row in product_perf_query
    ]

    # 6. Evolução do Ticket Médio
    ticket_query = db.query(
        cast(Order.created_at, Date).label('date'),
        func.avg(Order.total_amount).label('ticket')
    ).filter(
        Order.company_id == current_user.id,
        Order.payment_status == PaymentStatus.PAID,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).group_by(cast(Order.created_at, Date)).order_by(cast(Order.created_at, Date)).all()

    ticket_map = {row[0].strftime("%Y-%m-%d"): row[1] for row in ticket_query}
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