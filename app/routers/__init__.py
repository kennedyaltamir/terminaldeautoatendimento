# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 09:30:00

from .auth import router as auth_router
from .public import router as public_router
from .admin import router as admin_router
from .admin_menu import router as admin_menu_router
from .admin_company import router as admin_company_router
from .admin_tables import router as admin_tables_router
from .admin_metrics import router as admin_metrics_router
from .admin_inventory import router as admin_inventory_router
from .admin_employees import router as admin_employees_router
from .admin_billing import router as admin_billing_router
from .admin_delivery import router as admin_delivery_router
from .admin_audit import router as admin_audit_router
from .admin_fiscal import router as admin_fiscal_router
from .admin_financial import router as admin_financial_router
from .admin_history import router as admin_history_router  # NOVO
from .payments import router as payments_router
from .webhooks import router as webhooks_router

__all__ = [
    "auth", "public", "admin", "admin_menu", "admin_company", 
    "admin_tables", "admin_metrics", "admin_inventory", 
    "admin_employees", "admin_billing", "admin_delivery",
    "admin_audit", "admin_fiscal", "admin_financial", "admin_history",
    "payments", "webhooks"
]