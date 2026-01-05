import os
import json
import time
import sentry_sdk
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.database import get_db, engine
from app.websockets import manager
from app.core.limiter import limiter
from app.core.docs import tags_metadata, api_description

# Importações de Rotas
from app.routers import (
    auth, public, upload, admin_delivery, admin_logistics,
    admin_menu, admin_company, admin_tables, admin_metrics,
    admin_inventory, admin_employees, admin_billing, admin_audit,
    admin_fiscal, admin_financial, admin_marketing, admin_franchise,
    payments, webhooks, admin_payment, admin as admin_orders
)

# Configuração Sentry (Crucial para Render/Vercel)
sentry_dsn = os.getenv("SENTRY_DSN_BACKEND")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "production"),
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conectar Redis (Upstash/Managed) e verificar DB (Neon)
    await manager.startup()
    yield
    # Shutdown: Fechar conexões graciosamente
    await manager.shutdown()

app = FastAPI(
    title="MesaFlow API",
    description=api_description,
    version="2.3.1",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS ajustado para domínios de produção (Vercel)
origins = [
    "http://localhost:3000",
    "https://mesaflow.com.br",
    "https://*.vercel.app", # Suporte para Deploy Previews da Vercel
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINT DE SAÚDE PARA RENDER.COM ---
@app.get("/api/health", tags=["Integrations"])
async def health_check(db: Session = Depends(get_db)):
    """
    Realiza o diagnóstico de infraestrutura em nuvem.
    Render.com utiliza este endpoint para monitorar o status da aplicação.
    """
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "services": {
            "database": "down",
            "redis": "down"
        }
    }
    
    # 1. Verificar Neon.tech (PostgreSQL)
    try:
        start_time = time.time()
        db.execute(text("SELECT 1"))
        latency = (time.time() - start_time) * 1000
        health_status["services"]["database"] = f"up ({latency:.2f}ms)"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["database"] = f"error: {str(e)}"

    # 2. Verificar Redis (Upstash/Render Redis)
    if manager.use_redis and manager.redis_client:
        try:
            await manager.redis_client.ping()
            health_status["services"]["redis"] = "up"
        except Exception:
            health_status["status"] = "degraded"
            health_status["services"]["redis"] = "down"
    else:
        health_status["services"]["redis"] = "bypass (local memory)"

    return health_status

# --- INCLUSÃO DE ROTAS ---
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(public.router, prefix="/api", tags=["Public"])
app.include_router(upload.router, prefix="/api/upload", tags=["Integrations"])

# Admin Routers
app.include_router(admin_delivery.router, prefix="/api/admin/delivery", tags=["Admin Orders"])
app.include_router(admin_logistics.router, prefix="/api/admin/logistics", tags=["Admin Orders"])
app.include_router(admin_menu.router, prefix="/api/admin/menu", tags=["Admin Menu"])
app.include_router(admin_company.router, prefix="/api/admin/company", tags=["Admin Finance"])
app.include_router(admin_tables.router, prefix="/api/admin/tables", tags=["Admin Tables"])
app.include_router(admin_metrics.router, prefix="/api/admin/metrics", tags=["Admin Metrics"])
app.include_router(admin_inventory.router, prefix="/api/admin/inventory", tags=["Admin Menu"])
app.include_router(admin_employees.router, prefix="/api/admin/employees", tags=["Admin Finance"])
app.include_router(admin_billing.router, prefix="/api/admin/billing", tags=["Admin Finance"])
app.include_router(admin_audit.router, prefix="/api/admin/audit", tags=["Admin Metrics"])
app.include_router(admin_fiscal.router, prefix="/api/admin/fiscal", tags=["Admin Finance"])
app.include_router(admin_financial.router, prefix="/api/admin/financial", tags=["Admin Finance"])
app.include_router(admin_marketing.router, prefix="/api/admin/marketing", tags=["Admin Metrics"])
app.include_router(admin_franchise.router, prefix="/api/admin/franchise", tags=["Admin Metrics"])
app.include_router(admin_orders.router, prefix="/api/admin", tags=["Admin Orders"])
app.include_router(admin_payment.router, prefix="/api/admin/payment", tags=["Admin Finance"])

app.include_router(payments.router, prefix="/api/payments", tags=["Integrations"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Integrations"])

@app.websocket("/ws/{company_slug}")
async def websocket_endpoint(websocket: WebSocket, company_slug: str):
    await manager.connect(websocket, company_slug)
    try:
        while True:
            data_str = await websocket.receive_text()
            try:
                data = json.loads(data_str)
                if data.get("type") == "driver_location":
                    await manager.broadcast(data, company_slug)
                elif data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except json.JSONDecodeError:
                pass 
    except WebSocketDisconnect:
        manager.disconnect(websocket, company_slug)
    except Exception:
        manager.disconnect(websocket, company_slug)

@app.get("/")
def root():
    return {"message": "MesaFlow API v2.3.1 🚀", "health": "/api/health", "docs": "/docs"}
