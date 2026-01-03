import os
import sentry_sdk
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

# Importações
from app.routers import public
from app.routers import admin
from app.routers import auth
from app.routers import admin_menu
from app.routers import admin_company
from app.routers import admin_tables
from app.routers import admin_metrics
from app.routers import payments
from app.routers import webhooks
from app.routers import admin_inventory
from app.routers import admin_employees
from app.routers import admin_billing
from app.routers import admin_delivery
from app.routers import admin_audit
from app.routers import admin_fiscal
from app.routers import admin_financial
from app.routers import admin_marketing # NOVO

from app.websockets import manager
from app.core.limiter import limiter

# Configuração Sentry (Backend)
sentry_dsn = os.getenv("SENTRY_DSN_BACKEND")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0, # Ajustar para 0.1 em produção massiva
        environment=os.getenv("ENVIRONMENT", "development"),
        profiles_sample_rate=1.0,
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conecta ao Redis
    await manager.startup()
    yield
    # Shutdown: Desconecta
    await manager.shutdown()

app = FastAPI(
    title="MesaFlow API",
    description="API de Autoatendimento para Restaurantes",
    version="0.2.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.150:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROTAS ---
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(public.router, prefix="/api", tags=["Public"])

# Admin
app.include_router(admin_delivery.router, prefix="/api/admin/delivery", tags=["Admin Delivery"])
app.include_router(admin_menu.router, prefix="/api/admin/menu", tags=["Admin Menu"])
app.include_router(admin_company.router, prefix="/api/admin/company", tags=["Admin Company"])
app.include_router(admin_tables.router, prefix="/api/admin/tables", tags=["Admin Tables"])
app.include_router(admin_metrics.router, prefix="/api/admin/metrics", tags=["Admin Metrics"])
app.include_router(admin_inventory.router, prefix="/api/admin/inventory", tags=["Admin Inventory"])
app.include_router(admin_employees.router, prefix="/api/admin/employees", tags=["Admin Employees"])
app.include_router(admin_billing.router, prefix="/api/admin/billing", tags=["Admin Billing"])
app.include_router(admin_audit.router, prefix="/api/admin/audit", tags=["Admin Audit"])
app.include_router(admin_fiscal.router, prefix="/api/admin/fiscal", tags=["Admin Fiscal"])
app.include_router(admin_financial.router, prefix="/api/admin/financial", tags=["Admin Financial"])
app.include_router(admin_marketing.router, prefix="/api/admin/marketing", tags=["Admin Marketing"]) # NOVO

# Admin Genérico
app.include_router(admin.router, prefix="/api/admin", tags=["Admin Orders"])

app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])

@app.websocket("/ws/{company_slug}")
async def websocket_endpoint(websocket: WebSocket, company_slug: str):
    await manager.connect(websocket, company_slug)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, company_slug)
    except Exception:
        manager.disconnect(websocket, company_slug)

@app.get("/")
def root():
    return {"message": "MesaFlow API is running 🚀 (Redis + Sentry Enabled)"}

@app.get("/sentry-debug")
async def trigger_error():
    """Rota para testar se o Sentry está capturando erros"""
    division_by_zero = 1 / 0
    return division_by_zero