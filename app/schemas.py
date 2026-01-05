from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from typing import List, Optional, Any
from decimal import Decimal
from uuid import UUID
from datetime import time, datetime, date
import re

# --- VALIDATORS REUTILIZÁVEIS ---

def sanitize_html(v: str | None) -> str | None:
    """Remove tags HTML para prevenir XSS Stored"""
    if v is None:
        return None
    # Remove qualquer coisa entre < e >
    clean = re.sub(r'<[^>]*>', '', v)
    return clean.strip()

# --- AUTH & COMPANY ---

class SignUpRequest(BaseModel):
    company_name: str = Field(..., min_length=3)
    company_slug: str = Field(..., min_length=3, pattern="^[a-z0-9-]+$")
    owner_email: EmailStr
    password: str = Field(..., min_length=8)
    owner_phone: Optional[str] = None
    owner_role: Optional[str] = None
    segment: str = "gastro"

    @field_validator('company_name', 'owner_role')
    def sanitize(cls, v): return sanitize_html(v)

    @field_validator('password')
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Za-z]', v) or not re.search(r'[0-9]', v):
            raise ValueError('A senha deve conter letras e números')
        return v

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
    new_password: str = Field(..., min_length=8)

    @field_validator('new_password')
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Za-z]', v) or not re.search(r'[0-9]', v):
            raise ValueError('A senha deve conter letras e números')
        return v

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator('new_password')
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Za-z]', v) or not re.search(r'[0-9]', v):
            raise ValueError('A senha deve conter letras e números')
        return v

class CompanyPublic(BaseModel):
    name: str
    is_active: bool
    logo_url: Optional[str] = None
    primary_color: str = "#ea580c"
    banner_url: Optional[str] = None

    background_color: Optional[str] = "#f9fafb"
    text_color: Optional[str] = "#111827"
    accent_color: Optional[str] = "#ea580c"

    opens_at: Optional[time] = None
    closes_at: Optional[time] = None
    owner_email: Optional[str] = None
    pix_key: Optional[str] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    segment: str = "gastro"
    model_config = ConfigDict(from_attributes=True)

class CompanyAdminSettings(CompanyPublic):
    mp_access_token: Optional[str] = None
    marketplace_fee_percentage: Decimal = Decimal(0)
    loyalty_percentage: Decimal = Decimal(0)
    plan_tier: str = "free"
    trial_ends_at: Optional[datetime] = None
    stripe_subscription_id: Optional[str] = None
    subscription_status: Optional[str] = None

    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    fiscal_token: Optional[str] = None
    csc_token: Optional[str] = None
    csc_id: Optional[str] = None

    service_fee_percentage: Decimal = Decimal(10.0)
    fixed_delivery_fee: Decimal = Decimal(0.0)

    # Novos campos de Configuração de WhatsApp
    whatsapp_api_url: Optional[str] = None
    whatsapp_instance: Optional[str] = None
    whatsapp_token: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None

    primary_color: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    accent_color: Optional[str] = None

    opens_at: Optional[time] = None
    closes_at: Optional[time] = None
    pix_key: Optional[str] = None
    mp_access_token: Optional[str] = None
    loyalty_percentage: Optional[Decimal] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None

    # Novos campos de Configuração de WhatsApp
    whatsapp_api_url: Optional[str] = None
    whatsapp_instance: Optional[str] = None
    whatsapp_token: Optional[str] = None

    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None

    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    fiscal_token: Optional[str] = None
    csc_token: Optional[str] = None
    csc_id: Optional[str] = None

    service_fee_percentage: Optional[Decimal] = None
    fixed_delivery_fee: Optional[Decimal] = None

    @field_validator('name', 'wifi_ssid')
    def sanitize(cls, v): return sanitize_html(v)

    @field_validator('primary_color', 'background_color', 'text_color', 'accent_color')
    def validate_hex_color(cls, v):
        if v is not None:
            if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
                raise ValueError('Cor inválida. Use formato hexadecimal (ex: #FF0000)')
        return v

# --- MENU & PRODUCTS ---

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
    short_code: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
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

    @field_validator('name')
    def sanitize(cls, v): return sanitize_html(v)

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    order_index: Optional[int] = None
    availability_days: Optional[List[int]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

    @field_validator('name')
    def sanitize(cls, v): return sanitize_html(v)

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
    short_code: Optional[str] = None
    ncm: str = "21069090"
    cfop: str = "5102"
    recommended_ids: List[int] = []

    @field_validator('name', 'description', 'short_code')
    def sanitize(cls, v): return sanitize_html(v)

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
    short_code: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    recommended_ids: Optional[List[int]] = None

    @field_validator('name', 'description', 'short_code')
    def sanitize(cls, v): return sanitize_html(v)

class OptionGroupCreate(BaseModel):
    name: str
    min_selection: int = 0
    max_selection: int = 1

    @field_validator('name')
    def sanitize(cls, v): return sanitize_html(v)

class OptionCreate(BaseModel):
    name: str
    price: Decimal = Decimal(0)

    @field_validator('name')
    def sanitize(cls, v): return sanitize_html(v)

# --- ORDERS ---

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

class FeedbackResponse(BaseModel):
    score: int
    comment: Optional[str] = None
    created_at: datetime
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
    driver_id: Optional[int] = None

    fiscal_status: str = "pending"
    nfe_url_pdf: Optional[str] = None
    nfe_url_xml: Optional[str] = None

    service_fee: Decimal = Decimal(0)
    delivery_fee: Decimal = Decimal(0)
    
    feedback: Optional[FeedbackResponse] = None

    model_config = ConfigDict(from_attributes=True)

class OrderPagination(BaseModel):
    data: List[OrderResponse]
    total: int
    page: int
    limit: int

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    notes: Optional[str] = None
    selected_options: List[int] = []

    @field_validator('notes')
    def sanitize(cls, v): return sanitize_html(v)

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

    @field_validator('customer_name', 'delivery_address', 'customer_phone')
    def sanitize(cls, v): return sanitize_html(v)

class DispatchOrderRequest(BaseModel):
    driver_id: Optional[int] = None

class CompleteDeliveryRequest(BaseModel):
    code: Optional[str] = None

class FeedbackCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    
    @field_validator('comment')
    def sanitize(cls, v): return sanitize_html(v)

# --- TABLES & SESSIONS ---

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

class ServiceRequestCreate(BaseModel):
    table_id: int
    qr_token: str
    service_type: str
    notes: Optional[str] = None

    @field_validator('notes')
    def sanitize(cls, v): return sanitize_html(v)

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

    @field_validator('customer_name')
    def sanitize(cls, v): return sanitize_html(v)

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

    @field_validator('customer_name')
    def sanitize(cls, v): return sanitize_html(v)

class CloseTableRequest(BaseModel):
    payment_method: str

class TablePositionUpdate(BaseModel):
    id: int
    x: float
    y: float

class SessionUpdate(BaseModel):
    customer_name: str

    @field_validator('customer_name')
    def sanitize(cls, v): return sanitize_html(v)

class TableSessionDetail(BaseModel):
    id: int
    customer_name: str
    total_spent: Decimal
    start_time: datetime
    orders: List[OrderResponse]
    model_config = ConfigDict(from_attributes=True)

class TableTransferRequest(BaseModel):
    from_table_id: int
    to_table_id: int
    merge: bool = False

# --- INVENTORY & SUPPLIERS ---

class IngredientCreate(BaseModel):
    name: str
    unit: str = "un"
    current_stock: Decimal = Decimal(0)
    min_stock_alert: Decimal = Decimal(0)
    cost_per_unit: Decimal = Decimal(0)
    supplier_id: Optional[int] = None

    @field_validator('name')
    def sanitize(cls, v): return sanitize_html(v)

class IngredientResponse(BaseModel):
    id: int
    name: str
    unit: str
    current_stock: Decimal
    min_stock_alert: Decimal
    cost_per_unit: Decimal
    supplier_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class RecipeItemCreate(BaseModel):
    ingredient_id: int
    quantity_required: Decimal

class ProductRecipeUpdate(BaseModel):
    product_id: int
    ingredients: List[RecipeItemCreate]

class SupplierCreate(BaseModel):
    name: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator('name', 'contact_name')
    def sanitize(cls, v): return sanitize_html(v)

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ShoppingListItem(BaseModel):
    ingredient_name: str
    current_stock: Decimal
    min_stock: Decimal
    unit: str
    deficit: Decimal
    supplier_name: str
    model_config = ConfigDict(from_attributes=True)

class ShoppingListResponse(BaseModel):
    items: List[ShoppingListItem]

# --- EMPLOYEES ---

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=4)
    role: str = "kitchen"

    @field_validator('name')
    def sanitize(cls, v): return sanitize_html(v)

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('name')
    def sanitize(cls, v): return sanitize_html(v)

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- BILLING & METRICS ---

class StripeCheckoutResponse(BaseModel):
    url: str

class TopProduct(BaseModel):
    name: str
    count: int
    revenue: float

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
    top_products: List[Any]
    sales_chart: List[Any]
    sales_by_hour: List[Any]
    product_performance: List[Any]
    ticket_evolution: List[Any]

# --- AUDIT LOGS ---

class AuditLogResponse(BaseModel):
    id: int
    user_name: str
    user_role: str
    action: str
    resource: str
    resource_id: Optional[str] = None
    details: Optional[Any] = None
    ip_address: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- FISCAL ---

class FiscalEmissionResponse(BaseModel):
    status: str
    message: str
    nfe_url: Optional[str] = None

# --- FINANCIAL REPORTS ---

class TipReportItem(BaseModel):
    employee_name: str
    total_tips: float
    order_count: int

# --- LOGISTICS & DRIVER FINANCE ---

class DriverLedgerResponse(BaseModel):
    id: int
    type: str
    amount: Decimal
    description: Optional[str] = None
    created_at: datetime
    order_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)

class DriverBalanceResponse(BaseModel):
    driver_id: int
    driver_name: str
    current_debt: Decimal
    transactions: List[DriverLedgerResponse]
    model_config = ConfigDict(from_attributes=True)

class SettleDebtRequest(BaseModel):
    amount: Decimal
    description: Optional[str] = "Acerto de contas"

    @field_validator('description')
    def sanitize(cls, v): return sanitize_html(v)

class DriverRecommendation(BaseModel):
    driver_id: int
    name: str
    active_deliveries: int
    last_delivery_time: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# --- LEADS ---

class LeadCreate(BaseModel):
    email: EmailStr
    source: str = "landing_page"

class LeadResponse(BaseModel):
    message: str
    download_url: str
