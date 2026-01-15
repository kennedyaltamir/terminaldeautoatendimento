
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 01:25:00

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TopProduct(BaseModel):
    name: str
    count: int
    revenue: float
    model_config = ConfigDict(from_attributes=True)

class ChartData(BaseModel):
    date: str
    value: float

class SalesByHour(BaseModel):
    hour: int
    total: float
    count: int

class ProductPerformance(BaseModel):
    name: str
    revenue: float
    quantity: int

class TicketData(BaseModel):
    date: str
    ticket: float

class DashboardMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    average_ticket: float
    top_products: List[TopProduct]
    sales_chart: List[ChartData]
    sales_by_hour: List[SalesByHour]
    product_performance: List[ProductPerformance]
    ticket_evolution: List[TicketData] = []
    
    model_config = ConfigDict(from_attributes=True)

