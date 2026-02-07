# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-24 16:25:00
# DESCRIPTION: Exportação centralizada de Schemas para o Kernel.

from app.schemas.core import Monetary, OptionalMonetary, sanitize_html
from app.schemas.auth import (
    SignUpRequest, Token, TokenData, PasswordUpdate, 
    ForgotPasswordRequest, ResetPasswordRequest, DeviceRegister
)
from app.schemas.company import (
    CompanyPublic, CompanyAdminSettings, CompanyUpdate, KioskValidationRequest
)
from app.schemas.menu import (
    OptionResponse, OptionGroupResponse, ProductSimpleResponse, 
    ProductResponse, CategoryResponse, CategoryCreate, 
    CategoryUpdate, ProductCreate, ProductUpdate, 
    OptionGroupCreate, OptionCreate, MenuResponse
)
from app.schemas.orders import (
    # Table Requests
    TableCreate, TableBulkCreate, TablePositionUpdate, TableTransferRequest,
    # Table Responses
    TableSimpleResponse, TableResponse, TableDashboardResponse,
    # Session
    OpenTableRequest, CloseTableRequest, SessionUpdate, TableSessionDetail,
    # Order Requests
    OrderItemCreate, OrderCreate, DispatchOrderRequest, CompleteDeliveryRequest,
    # Order Responses
    OrderItemOptionResponse, OrderItemResponse, OrderResponse, OrderPagination,
    # Feedback & Service
    FeedbackCreate, FeedbackResponse, ServiceRequestResponse
)
from app.schemas.fintech import WalletResponse, TipReportItem, DriverLedgerResponse, DriverBalanceResponse, SettleDebtRequest, CouponValidationRequest, CouponValidationResponse, WebhookCreate, WebhookResponse, StripeCheckoutResponse, FiscalEmissionResponse
from app.schemas.public import CheckTableRequest, CheckTableResponse, TableSessionResponse, JoinTableRequest, LeadCreate, LeadResponse
from app.schemas.analytics import DashboardMetrics, ChartData, SalesByHour, ProductPerformance, TicketData, TopProduct
from app.schemas.inventory import SupplierCreate, SupplierResponse, IngredientCreate, IngredientResponse, ProductRecipeUpdate, ShoppingListResponse, ShoppingListItem
from app.schemas.staff import EmployeeBase, EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.schemas.system import AuditLogResponse, FeatureFlagUpdate, FeatureFlagResponse
from app.schemas.marketing import PromotionCreate, PromotionUpdate, PromotionResponse