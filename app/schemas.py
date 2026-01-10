# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 10:15:00
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator, PlainSerializer, BeforeValidator
from typing import List, Optional, Any, Annotated
from decimal import Decimal
from uuid import UUID
from datetime import time, datetime, date
import re

# --- CUSTOM TYPES (FINTECH PRECISION) ---

def decimal_to_cents(v: Decimal | None) -> int | None:
    if v is None: return None
    return int(round(v * 100))

def cents_to_decimal(v: int | float | Decimal | None) -> Decimal | None:
    if v is None: return None
    if isinstance(v, Decimal): return v
    return Decimal(str(v)) / 100

# Tipo Monetário: Entrada/Saída como Inteiro (Centavos), Interno como Decimal
Monetary = Annotated[
    Decimal,
    PlainSerializer(decimal_to_cents, return_type=int, when_used='json'),
    BeforeValidator(cents_to_decimal)
]

OptionalMonetary = Annotated[
    Optional[Decimal],
    PlainSerializer(decimal_to_cents, return_type=Optional[int], when_used='json'),
    BeforeValidator(cents_to_decimal)
]

# --- VALIDATORS REUTILIZÁVEIS ---

def sanitize_html(v: str | None) -> str | None:
    if v is None:
        return None
    clean = re.sub(r'<[^>]*>', '', v)
    return clean.strip()

# --- AUTH & COMPANY ---

class SignUpRequest(BaseModel):
    company_name: str = Field(..., min_length=3, example="Pizzaria do Bairro")
    company_slug: str = Field(..., min_length=3, pattern="^[a-z0-9-]+$", example="pizzaria-bairro")
    owner_email: EmailStr = Field(..., example="contato@pizzaria.com")
    password: str = Field(..., min_length=8, example="SenhaSegura123")
    owner_phone: Optional[str] = Field(None, example="5511999999999")
    owner_role: Optional[str] = Field(None, example="Gerente")
    segment: str = Field("gastro", example="gastro")

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

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

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
    payment_provider: str = "NONE"
    marketplace_fee_percentage: OptionalMonetary = Decimal(0)
    loyalty_percentage: OptionalMonetary = Decimal(0)
    plan_tier: str = "free"
    trial_ends_at: Optional[datetime] = None
    stripe_subscription_id: Optional[str] = None
    subscription_status: Optional[str] = None
    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    fiscal_token: Optional[str] = None
    csc_token: Optional[str] = None
    csc_id: Optional[str] = None
    service_fee_percentage: OptionalMonetary = Decimal(10.0)
    fixed_delivery_fee: OptionalMonetary = Decimal(0.0)
    whatsapp_api_url: Optional[str] = None
    whatsapp_instance: Optional[str] = None
    whatsapp_token: Optional[str] = None
    ifood_merchant_id: Optional[str] = None
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
    loyalty_percentage: OptionalMonetary = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
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
    service_fee_percentage: OptionalMonetary = None
    fixed_delivery_fee: OptionalMonetary = None
    ifood_merchant_id: Optional[str] = None
    ifood_token: Optional[str] = None

# --- MENU & PRODUCTS ---

class OptionResponse(BaseModel):
    id: int
    name: str
    price: Monetary
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
    price: Monetary
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Monetary
    image_url: Optional[str] = None
    is_available: bool
    track_stock: bool
    stock_quantity: int
    station: str = "kitchen"
    tags: List[str] = []
    short_code: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    external_id: Optional[str] = None
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
    name: str = Field(..., example="Lanches")
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
    category_id: int = Field(..., example=1)
    name: str = Field(..., example="X-Bacon")
    description: Optional[str] = Field(None, example="Pão, carne, queijo e bacon crocante")
    price: Monetary = Field(..., example=2590) # Centavos
    image_url: Optional[str] = None
    is_available: bool = True
    track_stock: bool = False
    stock_quantity: int = 0
    station: str = "kitchen"
    tags: List[str] = []
    short_code: Optional[str] = None
    ncm: str = "21069090"
    cfop: str = "5102"
    external_id: Optional[str] = None
    recommended_ids: List[int] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: OptionalMonetary = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    track_stock: Optional[bool] = None
    stock_quantity: Optional[int] = None
    station: Optional[str] = None
    tags: Optional[List[str]] = None
    short_code: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    external_id: Optional[str] = None
    recommended_ids: Optional[List[int]] = None

class OptionGroupCreate(BaseModel):
    name: str = Field(..., example="Escolha o Ponto")
    min_selection: int = 0
    max_selection: int = 1

class OptionCreate(BaseModel):
    name: str = Field(..., example="Bem Passado")
    price: Monetary = Decimal(0)

# --- ORDERS ---

class OrderItemOptionResponse(BaseModel):
    name: str
    price: Monetary
    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    id: int
    quantity: int = Field(..., example=1)
    notes: Optional[str] = Field(None, example="Sem cebola")
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
    id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    status: str = Field(..., example="pending")
    order_type: str = Field(..., example="dine_in")
    origin: str = Field(..., example="mesaflow")
    external_order_id: Optional[str] = None
    delivery_address: Optional[str] = None
    customer_phone: Optional[str] = None
    subtotal: OptionalMonetary = None
    discount_amount: Monetary = Decimal(0)
    cashback_earned: Monetary = Decimal(0)
    payment_method: str = Field(..., example="pix")
    payment_status: str = Field(..., example="paid")
    total_amount: Monetary = Field(..., example=4590)
    customer_name: Optional[str] = Field(None, example="João Silva")
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
    service_fee: Monetary = Decimal(0)
    delivery_fee: Monetary = Decimal(0)
    feedback: Optional[FeedbackResponse] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "accepted",
                "order_type": "delivery",
                "origin": "ifood",
                "total_amount": 5990,
                "customer_name": "Maria Oliveira",
                "created_at": "2026-01-05T19:00:00Z",
                "items": [
                    {"id": 1, "quantity": 1, "product": {"name": "Pizza Margherita"}}
                ]
            }
        }
    )

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
    coupon_code: Optional[str] = None

class DispatchOrderRequest(BaseModel):
    driver_id: Optional[int] = None

class CompleteDeliveryRequest(BaseModel):
    code: Optional[str] = None

class FeedbackCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

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

class ServiceRequestResponse(BaseModel):
    id: int
    table_number: int
    service_type: str
    notes: Optional[str] = None
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class WalletResponse(BaseModel):
    balance: Monetary
    loyalty_percentage: Monetary

class TableSessionResponse(BaseModel):
    id: int
    customer_name: str
    is_active: bool
    created_at: datetime
    orders: List[OrderResponse] = []
    total_spent: Monetary = Decimal(0)
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
    access_pin: Optional[str] = None
    requires_pin: bool = False

class JoinTableRequest(BaseModel):
    table_id: int
    qr_token: str
    customer_name: str
    pin: Optional[str] = None

class TableSessionSummary(BaseModel):
    id: int
    customer_name: str
    total_spent: Monetary
    start_time: datetime
    access_pin: Optional[str] = None
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
    custom_service_fee: OptionalMonetary = None

class TablePositionUpdate(BaseModel):
    id: int
    x: float
    y: float

class SessionUpdate(BaseModel):
    customer_name: str

class TableSessionDetail(BaseModel):
    id: int
    customer_name: str
    total_spent: Monetary
    start_time: datetime
    orders: List[OrderResponse]
    model_config = ConfigDict(from_attributes=True)

class TableTransferRequest(BaseModel):
    from_table_id: int
    to_table_id: int
    merge: bool = False

# --- INVENTORY & SUPPLIERS ---

class IngredientCreate(BaseModel):
    name: str = Field(..., example="Pão de Hambúrguer")
    unit: str = "un"
    current_stock: Decimal = Decimal(0)
    min_stock_alert: Decimal = Decimal(0)
    cost_per_unit: Monetary = Decimal(0)
    supplier_id: Optional[int] = None

class IngredientResponse(BaseModel):
    id: int
    name: str
    unit: str
    current_stock: Decimal
    min_stock_alert: Decimal
    cost_per_unit: Monetary
    supplier_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class RecipeItemCreate(BaseModel):
    ingredient_id: int
    quantity_required: Decimal

class ProductRecipeUpdate(BaseModel):
    product_id: int
    ingredients: List[RecipeItemCreate]

class SupplierCreate(BaseModel):
    name: str = Field(..., example="Distribuidora de Bebidas")
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
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
    name: str = Field(..., example="Carlos Garçom")
    email: EmailStr = Field(..., example="carlos@restaurante.com")
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
    amount: Monetary
    description: Optional[str] = None
    created_at: datetime
    order_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)

class DriverBalanceResponse(BaseModel):
    driver_id: int
    driver_name: str
    current_debt: Monetary
    transactions: List[DriverLedgerResponse]
    model_config = ConfigDict(from_attributes=True)

class SettleDebtRequest(BaseModel):
    amount: Monetary = Field(..., example=5000)
    description: Optional[str] = "Acerto de contas"

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

# --- MOBILE DEVICES ---

class DeviceRegister(BaseModel):
    fcm_token: str = Field(..., example="fcm_token_123...")
    device_name: Optional[str] = Field(None, example="Samsung S21")
    platform: Optional[str] = "android"

# --- WEBHOOKS ---

class WebhookCreate(BaseModel):
    target_url: str = Field(..., example="https://meu-erp.com/webhooks/mesaflow")
    events: List[str] = Field(..., example=["order.created", "order.updated"])
    secret: Optional[str] = Field(None, description="Segredo para assinatura HMAC. Se vazio, será gerado automaticamente.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "target_url": "https://webhook.site/my-id",
                "events": ["order.created", "order.updated"],
                "secret": "minha_chave_secreta_123"
            }
        }
    )

class WebhookResponse(BaseModel):
    id: int
    target_url: str
    events: List[str]
    secret: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- PROMOTIONS ---

class PromotionCreate(BaseModel):
    name: str = Field(..., example="Desconto de Verão")
    code: Optional[str] = Field(None, example="VERAO10")
    discount_type: str = Field("percentage", example="percentage")
    discount_value: Monetary = Field(..., example=1000)
    min_order_value: Monetary = Field(Decimal(0), example=5000)
    max_discount_value: OptionalMonetary = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Cupom Primeira Compra",
                "code": "BEMVINDO",
                "discount_type": "fixed",
                "discount_value": 1500,
                "min_order_value": 6000
            }
        }
    )

class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: OptionalMonetary = None
    min_order_value: OptionalMonetary = None
    max_discount_value: OptionalMonetary = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    is_active: Optional[bool] = None

class PromotionResponse(BaseModel):
    id: UUID
    name: str
    code: Optional[str] = None
    discount_type: str
    discount_value: Monetary
    min_order_value: Monetary
    max_discount_value: OptionalMonetary = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    current_usage: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class CouponValidationRequest(BaseModel):
    code: str = Field(..., example="VERAO10")
    total_amount: Monetary = Field(..., example=10000)

class CouponValidationResponse(BaseModel):
    valid: bool
    discount_amount: Monetary
    final_total: Monetary
    message: str
    promotion_id: Optional[UUID] = None

# --- FEATURE FLAGS ---

class FeatureFlagUpdate(BaseModel):
    key: str
    is_enabled: bool
