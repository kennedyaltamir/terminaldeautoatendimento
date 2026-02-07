# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-03 19:48:00
# DESCRIPTION: Modelo de pedidos atualizado com suporte a coordenadas GPS para logística.
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Numeric, Text, Index, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.core import GUID, OrderStatus, PaymentMethod, PaymentStatus, OrderType, OrderOrigin

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    qr_token = Column(String(64), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    position_x = Column(Numeric(5, 2), default=0) 
    position_y = Column(Numeric(5, 2), default=0)
    capacity = Column(Integer, default=4, nullable=False)
    company = relationship("Company", back_populates="tables")
    orders = relationship("Order", back_populates="table")
    sessions = relationship("TableSession", back_populates="table", cascade="all, delete-orphan")
    service_requests = relationship("ServiceRequest", back_populates="table", cascade="all, delete-orphan")
    __table_args__ = (Index("idx_company_table_unique", "company_id", "table_number", unique=True),)

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

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    service_type = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    table = relationship("Table", back_populates="service_requests")
    company = relationship("Company")

class Order(Base):
    __tablename__ = "orders"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    session_id = Column(Integer, ForeignKey("table_sessions.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    promotion_id = Column(GUID(), ForeignKey("promotions.id"), nullable=True)
    order_type = Column(String(50), default=OrderType.DINE_IN.value, nullable=False)
    origin = Column(String(50), default=OrderOrigin.MESAFLOW.value, nullable=False)
    
    pickup_note = Column(String(255), nullable=True) 
    external_order_id = Column(String(100), nullable=True, index=True)
    customer_name = Column(String(100))
    customer_phone = Column(String(20), nullable=True)
    delivery_address = Column(Text, nullable=True)
    
    # 🛰️ NOVAS COLUNAS: GEOLOCALIZAÇÃO
    delivery_lat = Column(Float, nullable=True)
    delivery_lng = Column(Float, nullable=True)
    
    delivery_code = Column(String(4), nullable=True)
    subtotal = Column(Numeric(10, 2), nullable=True)
    discount_amount = Column(Numeric(10, 2), default=0.0)
    cashback_earned = Column(Numeric(10, 2), default=0.0)
    service_fee = Column(Numeric(10, 2), default=0.0)
    delivery_fee = Column(Numeric(10, 2), default=0.0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), default=OrderStatus.PENDING.value, nullable=False)
    payment_method = Column(String(50), default=PaymentMethod.CASH.value)
    payment_status = Column(String(50), default=PaymentStatus.PENDING.value)
    
    # Integrações
    mp_payment_id = Column(String(100), nullable=True, index=True)
    mp_qr_code = Column(Text, nullable=True)
    mp_qr_code_base64 = Column(Text, nullable=True)
    
    # Fiscal
    fiscal_status = Column(String(50), default="pending")
    fiscal_reference_id = Column(String(100), nullable=True, index=True)
    nfe_key = Column(String(100), nullable=True)
    nfe_url_xml = Column(String(500), nullable=True)
    nfe_url_pdf = Column(String(500), nullable=True)
    
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
