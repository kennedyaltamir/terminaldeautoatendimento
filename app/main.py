import os
import json
import time
import asyncio
import sentry_sdk
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.database import get_db
from app.websockets import manager
from app.core.limiter import limiter
from app.core.docs import tags_metadata, api_description
from app.services.ifood_service import IfoodService

# Importações de Rotas
from app.routers import (
    auth, public, upload, admin_delivery, admin_logistics,
    admin_menu, admin_company, admin_tables, admin_metrics,
    admin_inventory, admin_employees, admin_billing, admin_audit,
    admin_fiscal, admin_financial, admin_marketing, admin_franchise,
    admin_integrations, admin_features,
    payments, webhooks, admin_payment, admin as admin_orders
)

# Configuração Sentry
sentry_dsn = os.getenv("SENTRY_DSN_BACKEND")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "production"),
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conectar Redis e verificar DB
    await manager.startup()
    
    # Iniciar Middleware iFood em background (Polling Service)
    ifood = IfoodService()
    asyncio.create_task(ifood.start_polling())
    
    yield
    # Shutdown: Fechar conexões graciosamente
    await manager.shutdown()

app = FastAPI(
    title="MesaFlow Enterprise API",
    description=api_description,
    version="3.1.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "MesaFlow Developer Support",
        "url": "https://mesaflow.com.br/developers",
        "email": "api@mesaflow.com.br",
    }
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS ajustado para domínios de produção
origins = [
    "http://localhost:3000",
    "https://mesaflow.com.br",
    "https://*.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", tags=["Infrastructure"], include_in_schema=False)
async def health_check(db: Session = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {"database": "down", "redis": "down"}
    }
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "up"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["database"] = f"error: {str(e)}"

    if manager.use_redis and manager.redis_client:
        try:
            await manager.redis_client.ping()
            health_status["services"]["redis"] = "up"
        except Exception:
            health_status["services"]["redis"] = "down"
    
    return health_status

# --- INCLUSÃO DE ROTAS ---

# Autenticação e Público
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(public.router, prefix="/api", tags=["Public API"])
app.include_router(upload.router, prefix="/api/upload", tags=["Media & Uploads"])

# Admin - Operação e Gestão
app.include_router(admin_features.router, prefix="/api/admin/features", tags=["Admin - Features"])
app.include_router(admin_orders.router, prefix="/api/admin", tags=["Admin - Orders"])
app.include_router(admin_menu.router, prefix="/api/admin/menu", tags=["Admin - Menu"])
app.include_router(admin_tables.router, prefix="/api/admin/tables", tags=["Admin - Tables"])
app.include_router(admin_inventory.router, prefix="/api/admin/inventory", tags=["Admin - Inventory"])
app.include_router(admin_delivery.router, prefix="/api/admin/delivery", tags=["Admin - Logistics"])
app.include_router(admin_logistics.router, prefix="/api/admin/logistics", tags=["Admin - Logistics"])
app.include_router(admin_employees.router, prefix="/api/admin/employees", tags=["Admin - Team"])
app.include_router(admin_audit.router, prefix="/api/admin/audit", tags=["Admin - BI & Metrics"])
app.include_router(admin_metrics.router, prefix="/api/admin/metrics", tags=["Admin - BI & Metrics"])
app.include_router(admin_marketing.router, prefix="/api/admin/marketing", tags=["Admin - Marketing"])
app.include_router(admin_franchise.router, prefix="/api/admin/franchise", tags=["Admin - Franchise"])
app.include_router(admin_integrations.router, prefix="/api/admin/integrations", tags=["Admin - Integrations & Webhooks"])

# SaaS - Financeiro e Fiscal
app.include_router(admin_company.router, prefix="/api/admin/company", tags=["SaaS - Billing & Settings"])
app.include_router(admin_billing.router, prefix="/api/admin/billing", tags=["SaaS - Billing & Settings"])
app.include_router(admin_payment.router, prefix="/api/admin/payment", tags=["SaaS - Billing & Settings"])
app.include_router(admin_fiscal.router, prefix="/api/admin/fiscal", tags=["SaaS - Fiscal"])
app.include_router(admin_financial.router, prefix="/api/admin/financial", tags=["SaaS - Financial Reports"])

# Webhooks Externos (Inbound)
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Inbound Webhooks"])
app.include_router(payments.router, prefix="/api/payments", tags=["Inbound Webhooks"])

@app.websocket("/ws/{company_slug}")
async def websocket_endpoint(websocket: WebSocket, company_slug: str):
    await manager.connect(websocket, company_slug)
    try:
        while True:
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, company_slug)
    except Exception:
        manager.disconnect(websocket, company_slug)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "MesaFlow API v3.1.0 🚀", "docs": "/docs"}
