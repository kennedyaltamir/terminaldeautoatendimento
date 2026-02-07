# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-02 09:15:00
# DESCRIPTION: Garante a exportação correta de todos os routers para o main.py

from .auth import router as auth_router
from .public import router as public_router
from .public_utils import router as public_utils_router
from .upload import router as upload_router
from .admin import router as admin_router
from .admin_company import router as admin_company_router
from .admin_employees import router as admin_employees_router
from .admin_features import router as admin_features_router
from .admin_menu import router as admin_menu_router
from .admin_tables import router as admin_tables_router
from .admin_delivery import router as admin_delivery_router
from .admin_logistics import router as admin_logistics_router
from .admin_inventory import router as admin_inventory_router
from .admin_billing import router as admin_billing_router
from .admin_payment import router as admin_payment_router
from .admin_fiscal import router as admin_fiscal_router
from .admin_financial import router as admin_financial_router
from .admin_metrics import router as admin_metrics_router
from .admin_audit import router as admin_audit_router
from .admin_history import router as admin_history_router
from .admin_marketing import router as admin_marketing_router
from .admin_franchise import router as admin_franchise_router
from .admin_ai import router as admin_ai_router
from .admin_integrations import router as admin_integrations_router
from .payments import router as payments_router
from .webhooks import router as webhooks_router
from .webhooks_ifood import router as webhooks_ifood_router
# 🛡️ FIX CRÍTICO: Exportação explícita do router mobile
from .logistics_mobile import router as logistics_mobile_router

__all__ = [
    "auth_router", "public_router", "public_utils_router", "upload_router",
    "admin_router", "admin_company_router", "admin_employees_router", "admin_features_router",
    "admin_menu_router", "admin_tables_router", "admin_delivery_router", "admin_logistics_router", "admin_inventory_router",
    "admin_billing_router", "admin_payment_router", "admin_fiscal_router", "admin_financial_router",
    "admin_metrics_router", "admin_audit_router", "admin_history_router", "admin_marketing_router", "admin_franchise_router", "admin_ai_router",
    "admin_integrations_router", "payments_router", "webhooks_router", "webhooks_ifood_router",
    "logistics_mobile_router"
]
