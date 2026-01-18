# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-16 13:15:00
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Text, Time, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.core import GUID, PlanTier, CompanySegment, PaymentProvider

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
    
    # Kiosk Security (L7)
    kiosk_password_hash = Column(String(255), nullable=True) # Se null, usa default 123456
    
    # Enum como String para evitar LookupError do SQLAlchemy
    plan_tier = Column(String(50), default=PlanTier.FREE.value, nullable=False)
    segment = Column(String(50), default=CompanySegment.GASTRO.value, nullable=False)
    
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
    
    payment_provider = Column(String(50), default=PaymentProvider.NONE.value, nullable=False)
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
    wallets = relationship("CustomerWallet", back_populates="company", cascade="all, delete-orphan")
    ingredients = relationship("Ingredient", back_populates="company", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="company", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="company", cascade="all, delete-orphan")
    service_ledger = relationship("ServiceFeeLedger", back_populates="company", cascade="all, delete-orphan")
    driver_ledger = relationship("DriverLedger", back_populates="company", cascade="all, delete-orphan")
    webhooks = relationship("WebhookSubscription", back_populates="company", cascade="all, delete-orphan")
    promotions = relationship("Promotion", back_populates="company", cascade="all, delete-orphan")
    feature_flags = relationship("FeatureFlag", back_populates="company", cascade="all, delete-orphan")
    feedbacks = relationship("OrderFeedback", back_populates="company", cascade="all, delete-orphan")

