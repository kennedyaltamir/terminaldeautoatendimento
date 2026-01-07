import uuid
from enum import Enum

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey,
    Enum as SQLEnum, Numeric, Text, Index, Time, Table as SQLTable, JSON
)
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app.database import Base 

# --- CUSTOM TYPES (SQLite Compatibility) ---

class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PGUUID())
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == 'postgresql':
            return str(value)
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value

# --- ENUMS (Todos com valores em lowercase) ---

class PlanTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class CompanySegment(str, Enum):
    GASTRO = "gastro"
    EVENT = "event"
    HOTEL = "hotel"
    CORP = "corp"

class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class PaymentMethod(str, Enum):
    PIX = "pix"
    CARD = "card"
    CASH = "cash"
    ONLINE = "online"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class OrderType(str, Enum):
    DINE_IN = "dine_in"
    DELIVERY = "delivery"
    TAKEOUT = "takeout"

class OrderOrigin(str, Enum):
    MESAFLOW = "mesaflow"
    IFOOD = "ifood"
    RAPPI = "rappi"

class ServiceType(str, Enum):
    HELP = "help"
    CLEANING = "cleaning"
    BILL = "bill"
    OTHER = "other"

class ProductStation(str, Enum):
    KITCHEN = "kitchen"
    BAR = "bar"
    DESSERT = "dessert"
    OTHER = "other"

class UnitOfMeasure(str, Enum):
    KG = "kg"
    G = "g"
    L = "l"
    ML = "ml"
    UN = "un"

class UserRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    CASHIER = "cashier"
    KITCHEN = "kitchen"
    DRIVER = "driver"

class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    IMPERSONATE = "impersonate"
    FEATURE_TOGGLE = "feature_toggle"

class FiscalStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    EMITTED = "emitted"
    ERROR = "error"
    CANCELED = "canceled"

class LedgerType(str, Enum):
    DEBT = "debt"
    CREDIT = "credit"
    PAYMENT = "payment"

class PaymentProvider(str, Enum):
    MERCADO_PAGO = "MERCADO_PAGO"
    EFI = "EFI"
    STRIPE = "STRIPE"
    PAGARME = "PAGARME"
    NONE = "NONE"

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    SHIPPING = "shipping"

# --- TABELAS DE ASSOCIAÇÃO ---

product_recommendations = SQLTable(
    'product_recommendations',
    Base.metadata,
    Column('source_product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('target_product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

# --- MODELS ---

class Company(Base):
    __tablename__ = "companies"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    custom_domain = Column(String(255), unique=True, nullable=True, index=True)
    owner_email = Column(String(255), nullable=False, index=True)
    owner_phone = Column(String(20), nullable=True)
    owner_role = Column(String(50), nullable=True)
    password_hash = Column(String(255), nullable=True)

    # Blindagem de Enums
    plan_tier = Column(SQLEnum(PlanTier, values_callable=lambda x: [e.value for e in x]), default=PlanTier.FREE, nullable=False)
    segment = Column(SQLEnum(CompanySegment, values_callable=lambda x: [e.value for e in x]), default=CompanySegment.GASTRO, nullable=False)
    
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    stripe_customer_id = Column(String(100), nullable=True, index=True)
    stripe_subscription_id = Column(String(100), nullable=True)
    subscription_status = Column(String(50), nullable=True)
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    primary_color = Column(String(7), default="#ea580c")
    background_color = Column(String(7), default="#f9fafb")
    text_color = Column(String(7), default="#111827")
    accent_color = Column(String(7), default="#ea580c")
    instagram_url = Column(String(255), nullable=True)
    whatsapp_number = Column(String(20), nullable=True)
    whatsapp_api_url = Column(String(500), nullable=True)
    whatsapp_instance = Column(String(100), nullable=True)
    whatsapp_token = Column(String(500), nullable=True)
    ifood_merchant_id = Column(String(100), nullable=True, index=True)
    ifood_token = Column(Text, nullable=True)
    wifi_ssid = Column(String(100), nullable=True)
    wifi_password = Column(String(100), nullable=True)

    payment_provider = Column(SQLEnum(PaymentProvider, values_callable=lambda x: [e.value for e in x]), default=PaymentProvider.NONE, nullable=False)
    payment_credentials = Column(JSON, nullable=True) 
    pix_key = Column(String(255), nullable=True)
    mp_access_token = Column(String(255), nullable=True)
    mp_user_id = Column(String(50), nullable=True)
    marketplace_fee_percentage = Column(Numeric(5, 2), default=0.0)
    pending_commission_balance = Column(Numeric(10, 2), default=0.00)
    loyalty_percentage = Column(Numeric(5, 2), default=0.0)
    service_fee_percentage = Column(Numeric(5, 2), default=10.0)
    fixed_delivery_fee = Column(Numeric(10, 2), default=0.00)
    cnpj = Column(String(20), nullable=True)
    inscricao_estadual = Column(String(20), nullable=True)
    fiscal_token = Column(String(255), nullable=True)
    csc_token = Column(String(100), nullable=True)
    csc_id = Column(String(10), nullable=True)
    opens_at = Column(Time, nullable=True)
    closes_at = Column(Time, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tables = relationship("Table", back_populates="company", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="company", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="company")
    service_requests = relationship("ServiceRequest", back_populates="company", cascade="all, delete-orphan")
    wallets = relationship("CustomerWallet", back_populates="company", cascade="all, delete-orphan")
    ingredients = relationship("Ingredient", back_populates="company", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="company", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="company", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="company", cascade="all, delete-orphan")
    service_ledger = relationship("ServiceFeeLedger", back_populates="company", cascade="all, delete-orphan")
    driver_ledger = relationship("DriverLedger", back_populates="company", cascade="all, delete-orphan")
    feedbacks = relationship("OrderFeedback", back_populates="company", cascade="all, delete-orphan")
    devices = relationship("UserDevice", back_populates="company", cascade="all, delete-orphan")
    webhooks = relationship("WebhookSubscription", back_populates="company", cascade="all, delete-orphan")
    promotions = relationship("Promotion", back_populates="company", cascade="all, delete-orphan")
    feature_flags = relationship("FeatureFlag", back_populates="company", cascade="all, delete-orphan")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole, values_callable=lambda x: [e.value for e in x]), default=UserRole.KITCHEN, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="employees")
    deliveries = relationship("Order", back_populates="driver")
    tips = relationship("ServiceFeeLedger", back_populates="employee")
    driver_transactions = relationship("DriverLedger", back_populates="driver")
    devices = relationship("UserDevice", back_populates="employee", cascade="all, delete-orphan")
    __table_args__ = (Index("idx_employee_email", "email", unique=True),)

class UserDevice(Base):
    __tablename__ = "user_devices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    fcm_token = Column(String(255), nullable=False, unique=True)
    device_name = Column(String(100), nullable=True)
    platform = Column(String(20), default="android")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="devices")
    employee = relationship("Employee", back_populates="devices")

class WebhookSubscription(Base):
    __tablename__ = "webhook_subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    target_url = Column(String(500), nullable=False)
    events = Column(JSON, nullable=False) 
    secret = Column(String(100), nullable=False) 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="webhooks")

class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    key = Column(String(100), nullable=False, index=True)
    is_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="feature_flags")
    __table_args__ = (Index("idx_company_feature_key", "company_id", "key", unique=True),)

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    qr_token = Column(String(64), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    position_x = Column(Numeric(5, 2), default=0) 
    position_y = Column(Numeric(5, 2), default=0)

    company = relationship("Company", back_populates="tables")
    orders = relationship("Order", back_populates="table")
    sessions = relationship("TableSession", back_populates="table", cascade="all, delete-orphan")
    __table_args__ = (Index("idx_company_table_unique", "company_id", "table_number", unique=True),)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    order_index = Column(Integer, default=0)
    availability_days = Column(JSON, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)

    company = relationship("Company", back_populates="categories")
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String(500))
    is_available = Column(Boolean, default=True)
    short_code = Column(String(10), nullable=True, index=True)
    track_stock = Column(Boolean, default=False)
    stock_quantity = Column(Integer, default=0)
    station = Column(SQLEnum(ProductStation, values_callable=lambda x: [e.value for e in x]), default=ProductStation.KITCHEN, nullable=False)
    tags = Column(JSON, default=[])
    ncm = Column(String(10), default="21069090")
    cfop = Column(String(5), default="5102")
    external_id = Column(String(100), nullable=True, index=True)

    category = relationship("Category", back_populates="products")
    option_groups = relationship("OptionGroup", back_populates="product", cascade="all, delete-orphan")
    recipe_items = relationship("ProductRecipe", back_populates="product", cascade="all, delete-orphan")
    recommendations = relationship(
        "Product",
        secondary=product_recommendations,
        primaryjoin=id==product_recommendations.c.source_product_id,
        secondaryjoin=id==product_recommendations.c.target_product_id,
        backref="recommended_by"
    )

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

    company = relationship("Company", back_populates="suppliers")
    ingredients = relationship("Ingredient", back_populates="supplier")

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    name = Column(String(255), nullable=False)
    unit = Column(SQLEnum(UnitOfMeasure, values_callable=lambda x: [e.value for e in x]), default=UnitOfMeasure.UN, nullable=False)
    current_stock = Column(Numeric(10, 3), default=0.000)
    min_stock_alert = Column(Numeric(10, 3), default=0.000)
    cost_per_unit = Column(Numeric(10, 2), default=0.00)

    company = relationship("Company", back_populates="ingredients")
    supplier = relationship("Supplier", back_populates="ingredients")
    product_links = relationship("ProductRecipe", back_populates="ingredient")

class ProductRecipe(Base):
    __tablename__ = "product_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity_required = Column(Numeric(10, 3), nullable=False)

    product = relationship("Product", back_populates="recipe_items")
    ingredient = relationship("Ingredient", back_populates="product_links")

class OptionGroup(Base):
    __tablename__ = "option_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String(100), nullable=False)
    min_selection = Column(Integer, default=0)
    max_selection = Column(Integer, default=1)
    product = relationship("Product", back_populates="option_groups")
    options = relationship("Option", back_populates="group", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("option_groups.id"), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), default=0)
    is_available = Column(Boolean, default=True)
    group = relationship("OptionGroup", back_populates="options")

class TableSession(Base):
    __tablename__ = "table_sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False)
    opened_by_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=True)
    session_token = Column(String(64), nullable=False, unique=True, index=True)
    access_pin = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    company = relationship("Company")
    table = relationship("Table", back_populates="sessions")
    orders = relationship("Order", back_populates="session")
    opener = relationship("Employee")

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=True) 
    discount_type = Column(SQLEnum(DiscountType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    min_order_value = Column(Numeric(10, 2), default=0.00)
    max_discount_value = Column(Numeric(10, 2), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    usage_limit = Column(Integer, nullable=True)
    current_usage = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="promotions")
    orders = relationship("Order", back_populates="promotion")

    __table_args__ = (
        Index("idx_promotions_code", "company_id", "code", unique=True),
    )

class Order(Base):
    __tablename__ = "orders"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    session_id = Column(Integer, ForeignKey("table_sessions.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    promotion_id = Column(GUID(), ForeignKey("promotions.id"), nullable=True)

    order_type = Column(SQLEnum(OrderType, values_callable=lambda x: [e.value for e in x]), default=OrderType.DINE_IN, nullable=False)
    origin = Column(SQLEnum(OrderOrigin, values_callable=lambda x: [e.value for e in x]), default=OrderOrigin.MESAFLOW, nullable=False)
    external_order_id = Column(String(100), nullable=True, index=True)

    customer_phone = Column(String(20), nullable=True)
    delivery_address = Column(Text, nullable=True)
    delivery_code = Column(String(4), nullable=True)

    subtotal = Column(Numeric(10, 2), nullable=True)
    discount_amount = Column(Numeric(10, 2), default=0.0)
    cashback_earned = Column(Numeric(10, 2), default=0.0)
    service_fee = Column(Numeric(10, 2), default=0.0)
    delivery_fee = Column(Numeric(10, 2), default=0.0)

    status = Column(SQLEnum(OrderStatus, values_callable=lambda x: [e.value for e in x]), default=OrderStatus.PENDING, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod, values_callable=lambda x: [e.value for e in x]), default=PaymentMethod.CASH)
    payment_status = Column(SQLEnum(PaymentStatus, values_callable=lambda x: [e.value for e in x]), default=PaymentStatus.PENDING)

    mp_payment_id = Column(String(100), nullable=True, index=True)
    mp_qr_code = Column(Text, nullable=True)
    mp_qr_code_base64 = Column(Text, nullable=True)

    fiscal_status = Column(String(50), default="pending")
    fiscal_reference_id = Column(String(100), nullable=True, index=True)
    nfe_key = Column(String(100), nullable=True)
    nfe_url_xml = Column(String(500), nullable=True)
    nfe_url_pdf = Column(String(500), nullable=True)

    customer_name = Column(String(100))
    total_amount = Column(Numeric(10, 2), nullable=False)
    device_fingerprint = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

    company = relationship("Company", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    session = relationship("TableSession", back_populates="orders")
    driver = relationship("Employee", back_populates="deliveries")
    driver_ledger_entries = relationship("DriverLedger", back_populates="order")
    feedback = relationship("OrderFeedback", uselist=False, back_populates="order", cascade="all, delete-orphan")
    promotion = relationship("Promotion", back_populates="orders")

    __table_args__ = (
        Index("idx_orders_company_status", "company_id", "status"),
        Index("idx_orders_company_created", "company_id", "created_at"),
    )

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    selected_options = relationship("OrderItemOption", back_populates="order_item", cascade="all, delete-orphan")

    __table_args__ = (Index("idx_order_items_order_id", "order_id"),)

class OrderItemOption(Base):
    __tablename__ = "order_item_options"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=False)
    name = Column(String(100))
    price = Column(Numeric(10, 2))
    order_item = relationship("OrderItem", back_populates="selected_options")

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    service_type = Column(SQLEnum(ServiceType, values_callable=lambda x: [e.value for e in x]), default=ServiceType.HELP, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="service_requests")
    table = relationship("Table")

class CustomerWallet(Base):
    __tablename__ = "customer_wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    company = relationship("Company", back_populates="wallets")
    __table_args__ = (Index("idx_wallet_unique", "company_id", "customer_phone", unique=True),)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    user_name = Column(String(100), nullable=False)
    user_role = Column(String(50), nullable=False)
    action = Column(SQLEnum(AuditAction, values_callable=lambda x: [e.value for e in x]), nullable=False)
    resource = Column(String(50), nullable=False)
    resource_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="audit_logs")
    __table_args__ = (Index("idx_audit_logs_company_created", "company_id", "created_at"),)

class ServiceFeeLedger(Base):
    __tablename__ = "service_fee_ledger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="service_ledger")
    employee = relationship("Employee", back_populates="tips")

class DriverLedger(Base):
    __tablename__ = "driver_ledger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=True)
    type = Column(SQLEnum(LedgerType, values_callable=lambda x: [e.value for e in x]), nullable=False) 
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="driver_ledger")
    driver = relationship("Employee", back_populates="driver_transactions")
    order = relationship("Order", back_populates="driver_ledger_entries")

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, index=True)
    source = Column(String(50), default="landing_page")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(255), nullable=False, index=True)
    token = Column(String(64), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OrderFeedback(Base):
    __tablename__ = "order_feedbacks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(GUID(), ForeignKey("orders.id"), unique=True, nullable=False)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    score = Column(Integer, nullable=False) 
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="feedback")
    company = relationship("Company", back_populates="feedbacks")
