from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List, Optional
from decimal import Decimal
from uuid import UUID
from datetime import time, datetime

class SignUpRequest(BaseModel):
    company_name: str = Field(..., min_length=3)
    company_slug: str = Field(..., min_length=3, pattern="^[a-z0-9-]+$")
    owner_email: EmailStr
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    company_slug: str
    company_name: str
    user_role: str
    user_name: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)

class CompanyPublic(BaseModel):
    name: str
    is_active: bool
    logo_url: Optional[str] = None
    primary_color: str = "#ea580c"
    banner_url: Optional[str] = None
    opens_at: Optional[time] = None
    closes_at: Optional[time] = None
    owner_email: Optional[str] = None
    pix_key: Optional[str] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CompanyAdminSettings(CompanyPublic):
    mp_access_token: Optional[str] = None
    marketplace_fee_percentage: Decimal = Decimal(0)
    loyalty_percentage: Decimal = Decimal(0)
    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    banner_url: Optional[str] = None
    opens_at: Optional[time] = None
    closes_at: Optional[time] = None
    pix_key: Optional[str] = None
    mp_access_token: Optional[str] = None
    loyalty_percentage: Optional[Decimal] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None

class OptionResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    is_available: bool
    model_config = ConfigDict(from_attributes=True)

class OptionGroupResponse(BaseModel):
    id: int
    name: str
    min_selection: int
    max_selection: int
    options: List[OptionResponse]
    model_config = ConfigDict(from_attributes=True)

class ProductSimpleResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    is_available: bool
    track_stock: bool
    stock_quantity: int
    station: str = "kitchen"
    tags: List[str] = []
    option_groups: List[OptionGroupResponse] = []
    recommendations: List[ProductSimpleResponse] = []
    model_config = ConfigDict(from_attributes=True)

class CategoryResponse(BaseModel):
    id: int
    name: str
    products: List[ProductResponse]
    availability_days: Optional[List[int]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    model_config = ConfigDict(from_attributes=True)

class MenuResponse(BaseModel):
    company: CompanyPublic
    categories: List[CategoryResponse]

class CategoryCreate(BaseModel):
    name: str
    order_index: int = 0
    availability_days: Optional[List[int]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    order_index: Optional[int] = None
    availability_days: Optional[List[int]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    is_available: bool = True
    track_stock: bool = False
    stock_quantity: int = 0
    station: str = "kitchen"
    tags: List[str] = []
    recommended_ids: List[int] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    track_stock: Optional[bool] = None
    stock_quantity: Optional[int] = None
    station: Optional[str] = None
    tags: Optional[List[str]] = None
    recommended_ids: Optional[List[int]] = None

class OptionGroupCreate(BaseModel):
    name: str
    min_selection: int = 0
    max_selection: int = 1

class OptionCreate(BaseModel):
    name: str
    price: Decimal = Decimal(0)

class OrderItemOptionResponse(BaseModel):
    name: str
    price: Decimal
    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    notes: Optional[str] = None
    product: ProductResponse
    selected_options: List[OrderItemOptionResponse] = []
    model_config = ConfigDict(from_attributes=True)

class TableSimpleResponse(BaseModel):
    table_number: int
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    status: str
    order_type: str
    delivery_address: Optional[str] = None
    customer_phone: Optional[str] = None
    subtotal: Optional[Decimal] = None
    discount_amount: Decimal = Decimal(0)
    cashback_earned: Decimal = Decimal(0)
    payment_method: str
    payment_status: str
    total_amount: Decimal
    customer_name: Optional[str]
    created_at: datetime
    finished_at: Optional[datetime] = None
    table: Optional[TableSimpleResponse] = None
    items: List[OrderItemResponse] = []
    mp_qr_code: Optional[str] = None
    mp_qr_code_base64: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    notes: Optional[str] = None
    selected_options: List[int] = []

class OrderCreate(BaseModel):
    table_id: Optional[int] = None
    qr_token: Optional[str] = None
    order_type: str = "dine_in"
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    customer_name: Optional[str] = "Cliente"
    payment_method: str = "cash"
    use_balance: bool = False
    items: List[OrderItemCreate]

class TableResponse(BaseModel):
    id: int
    table_number: int
    qr_token: str
    is_active: bool
    position_x: float = 0
    position_y: float = 0
    model_config = ConfigDict(from_attributes=True)

class TableCreate(BaseModel):
    table_number: int

class TableBulkCreate(BaseModel):
    start: int
    end: int

class TopProduct(BaseModel):
    name: str
    count: int

class ChartData(BaseModel):
    date: str
    value: Decimal

class ServiceRequestCreate(BaseModel):
    table_id: int
    qr_token: str
    service_type: str
    notes: Optional[str] = None

class ServiceRequestResponse(BaseModel):
    id: int
    table_number: int
    service_type: str
    notes: Optional[str] = None
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class WalletResponse(BaseModel):
    balance: Decimal
    loyalty_percentage: Decimal

class TableSessionResponse(BaseModel):
    id: int
    customer_name: str
    is_active: bool
    created_at: datetime
    orders: List[OrderResponse] = []
    total_spent: Decimal = Decimal(0)
    access_pin: str
    model_config = ConfigDict(from_attributes=True)

class CheckTableRequest(BaseModel):
    table_id: int
    qr_token: str
    session_token: Optional[str] = None

class CheckTableResponse(BaseModel):
    status: str
    customer_name: Optional[str] = None
    session_token: Optional[str] = None
    requires_pin: bool = False

class JoinTableRequest(BaseModel):
    table_id: int
    qr_token: str
    customer_name: str
    pin: Optional[str] = None

class TableSessionSummary(BaseModel):
    id: int
    customer_name: str
    total_spent: Decimal
    start_time: datetime
    model_config = ConfigDict(from_attributes=True)

class TableDashboardResponse(BaseModel):
    id: int
    table_number: int
    qr_token: str
    status: str
    position_x: float = 0
    position_y: float = 0
    active_session: Optional[TableSessionSummary] = None
    service_request: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OpenTableRequest(BaseModel):
    customer_name: str

class CloseTableRequest(BaseModel):
    payment_method: str

class TablePositionUpdate(BaseModel):
    id: int
    x: float
    y: float

class IngredientCreate(BaseModel):
    name: str
    unit: str = "un"
    current_stock: Decimal = Decimal(0)
    min_stock_alert: Decimal = Decimal(0)
    cost_per_unit: Decimal = Decimal(0)

class IngredientResponse(BaseModel):
    id: int
    name: str
    unit: str
    current_stock: Decimal
    min_stock_alert: Decimal
    cost_per_unit: Decimal
    model_config = ConfigDict(from_attributes=True)

class RecipeItemCreate(BaseModel):
    ingredient_id: int
    quantity_required: Decimal

class ProductRecipeUpdate(BaseModel):
    product_id: int
    ingredients: List[RecipeItemCreate]

class SalesByHour(BaseModel):
    hour: int
    total: Decimal
    count: int

class ProductPerformance(BaseModel):
    name: str
    revenue: Decimal
    quantity: int

class TicketData(BaseModel):
    date: str
    ticket: Decimal

class DashboardMetrics(BaseModel):
    total_revenue: Decimal
    total_orders: int
    average_ticket: Decimal
    top_products: List[TopProduct]
    sales_chart: List[ChartData]
    sales_by_hour: List[SalesByHour] = []
    product_performance: List[ProductPerformance] = []
    ticket_evolution: List[TicketData] = []

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=4)
    role: str = "kitchen"

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)