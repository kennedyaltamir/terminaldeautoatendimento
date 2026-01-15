
# DOMAIN: BACKEND [CRITICAL_PATH]
# LAST_MODIFIED: 2026-01-11 00:55:00

# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11
# ESTE ARQUIVO FOI MODULARIZADO PARA app/models/*.py
# MANTIDO APENAS PARA COMPATIBILIDADE DE IMPORTAÇÃO LEGADA
from app.models.core import (
    GUID, PlanTier, CompanySegment, OrderStatus, PaymentMethod, 
    PaymentStatus, OrderType, OrderOrigin, ServiceType, 
    ProductStation, UnitOfMeasure, UserRole, AuditAction, 
    FiscalStatus, LedgerType, PaymentProvider, DiscountType
)
from app.models.company import Company
from app.models.auth import Employee, UserDevice
from app.models.menu import (
    Category, Product, OptionGroup, Option, 
    Ingredient, ProductRecipe, Supplier, product_recommendations
)
from app.models.orders import (
    Table, TableSession, ServiceRequest, Order, OrderItem, OrderItemOption
)
from app.models.fintech import (
    CustomerWallet, ServiceFeeLedger, DriverLedger, PaymentTransaction
)
from app.models.public import Lead, OrderFeedback, PasswordResetToken
from app.models.system import AuditLog, WebhookSubscription, FeatureFlag
from app.models.marketing import Promotion

