# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 01:00:00
import uuid
from enum import Enum
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, text, Table
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.database import Base
"""
🛡️ SECURITY POLICY: ROW-LEVEL SECURITY (RLS)
This application enforces strict multi-tenant isolation at the database level.
THREAT MODEL:
1. Application Layer Compromise: If the API is breached, RLS prevents cross-tenant data leakage.
2. Human Error: Developers forgetting a .filter(company_id) will be blocked by the DB engine.
3. Authorization Bugs: RBAC failures are mitigated by the session-bound app.current_company_id.
IMPLEMENTATION:
All core tables must have a 'company_id' column and a corresponding PostgreSQL Policy
linked to the 'app.current_company_id' session variable.
"""
class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as string.
    """
    impl = CHAR
    cache_ok = True
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PGUUID())
        else:
            return dialect.type_descriptor(CHAR(36))
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        else:
            return value
# RFC-008: Centralized Association Tables
product_recommendations = Table(
    'product_recommendations',
    Base.metadata,
    Column('source_product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('target_product_id', Integer, ForeignKey('products.id'), primary_key=True),
    extend_existing=True
)
# RFC-009 COMPLIANT ENUMS (LOWERCASE VALUES)
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
    MERCADO_PAGO = "mercadopago"
    EFI = "efi"
    STRIPE = "stripe"
    PAGARME = "pagarme"
    NONE = "none"
class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    SHIPPING = "shipping"