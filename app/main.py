# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-14 19:40:00
import os
import json
import time
import asyncio
import sentry_sdk
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from app.database import get_db, SessionLocal
from app.websockets import manager
from app.core.limiter import limiter
from app.core.docs import tags_metadata, api_description
from app.core.logger import logger
from app.services.ifood_service import IfoodService
from app.core.circuit_breaker import CircuitBreaker
# Importações de Rotas
from app.routers import (
    auth, public, upload, admin_delivery, admin_logistics,
    admin_menu, admin_company, admin_tables, admin_metrics,
    admin_inventory, admin_employees, admin_billing, admin_audit,
    admin_fiscal, admin_financial, admin_marketing, admin_franchise,
    admin_integrations, admin_features, admin_ai, admin_history, 
    payments, webhooks, admin_payment, admin as admin_orders,
    webhooks_ifood
)
# Configuração Sentry (Produção)
sentry_dsn = os.getenv("SENTRY_DSN_BACKEND")
environment = os.getenv("ENVIRONMENT", "production")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=environment,
        traces_sample_rate=1.0 if environment == "development" else 0.1,
        profiles_sample_rate=1.0 if environment == "development" else 0.1,
        send_default_pii=False,
    )
    logger.info(f"Sentry inicializado no ambiente: {environment}")
else:
    logger.warning("SENTRY_DSN_BACKEND não configurado. Observabilidade reduzida.")
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando MesaFlow API...")
    await manager.startup()
    ifood = IfoodService()
    asyncio.create_task(ifood.start_polling())
    yield
    logger.info("Encerrando MesaFlow API...")
    await manager.shutdown()
app = FastAPI(
    title="MesaFlow Enterprise API",
    description=api_description,
    version="3.3.7",
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
# Middleware de Segurança (Enterprise Hardening - TASK-GTM-07)
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    csp_policy = (
        "default-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'self';"
    )
    response.headers["Content-Security-Policy"] = csp_policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=()"
    return response
# Middleware de Contexto para Sentry e Logs
@app.middleware("http")
async def add_process_context(request: Request, call_next):
    if request.url.path.endswith(("/health", "/docs", "/openapi.json", "/favicon.ico")):
        return await call_next(request)
    try:
        await CircuitBreaker.check_health()
    except Exception as e:
        return Response(
            content=json.dumps({"detail": str(e), "code": "CIRCUIT_OPEN"}),
            status_code=503,
            media_type="application/json"
        )
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        log_data = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": f"{process_time:.4f}s",
            "client_ip": request.client.host if request.client else "unknown"
        }
        if response.status_code >= 400:
            logger.warning(f"Request Failed: {json.dumps(log_data)}")
            if response.status_code >= 500:
                CircuitBreaker.record_error()
            elif response.status_code >= 400 and response.status_code not in [401, 403]:
                CircuitBreaker.record_error()
        else:
            logger.info(f"Request Processed: {json.dumps(log_data)}")
            CircuitBreaker.record_success()
        return response
    except Exception as e:
        CircuitBreaker.record_error()
        logger.error(f"💥 UNHANDLED_EXCEPTION: {str(e)}")
        raise e
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.150:3000",
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
# --- HEALTH CHECK ---
@app.get("/health", tags=["Infrastructure"], include_in_schema=False)
@app.get("/api/health", tags=["Infrastructure"], include_in_schema=False)
async def health_check():
    # FIX: Removido Depends(get_db) para evitar erro 500 quando DB cai.
    # O health check deve reportar "unhealthy" (200 OK) ao invés de crashar.
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {"database": "down", "redis": "down"}
    }
    try:
        # Cria sessão manual segura
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            health_status["services"]["database"] = "up"
        finally:
            db.close()
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["database"] = f"error: {str(e)}"
        logger.error(f"Health Check DB Failed: {e}")
    if manager.use_redis and manager.redis_client:
        try:
            await manager.redis_client.ping()
            health_status["services"]["redis"] = "up"
        except Exception as e:
            health_status["services"]["redis"] = "down"
            logger.error(f"Health Check Redis Failed: {e}")
    return health_status
# --- INCLUSÃO DE ROTAS ---
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(public.router, prefix="/api", tags=["Public API"])
app.include_router(upload.router, prefix="/api/upload", tags=["Media & Uploads"])
app.include_router(admin_features.router, prefix="/api/admin/features", tags=["Admin - Features"])
app.include_router(admin_orders.router, prefix="/api/admin", tags=["Admin - Orders"])
app.include_router(admin_menu.router, prefix="/api/admin/menu", tags=["Admin - Menu"])
app.include_router(admin_tables.router, prefix="/api/admin", tags=["Admin - Tables"]) 
app.include_router(admin_inventory.router, prefix="/api/admin/inventory", tags=["Admin - Inventory"])
app.include_router(admin_delivery.router, prefix="/api/admin/delivery", tags=["Admin - Logistics"])
app.include_router(admin_logistics.router, prefix="/api/admin/logistics", tags=["Admin - Logistics"])
app.include_router(admin_employees.router, prefix="/api/admin/employees", tags=["Admin - Team"])
app.include_router(admin_audit.router, prefix="/api/admin/audit", tags=["Admin - BI & Metrics"])
app.include_router(admin_metrics.router, prefix="/api/admin/metrics", tags=["Admin - BI & Metrics"])
app.include_router(admin_marketing.router, prefix="/api/admin/marketing", tags=["Admin - Marketing"])
app.include_router(admin_franchise.router, prefix="/api/admin/franchise", tags=["Admin - Franchise"])
app.include_router(admin_integrations.router, prefix="/api/admin/integrations", tags=["Admin - Integrations & Webhooks"])
app.include_router(admin_company.router, prefix="/api/admin/company", tags=["SaaS - Billing & Settings"])
app.include_router(admin_billing.router, prefix="/api/admin/billing", tags=["SaaS - Billing & Settings"])
app.include_router(admin_payment.router, prefix="/api/admin/payment", tags=["SaaS - Billing & Settings"])
app.include_router(admin_fiscal.router, prefix="/api/admin/fiscal", tags=["SaaS - Fiscal"])
app.include_router(admin_financial.router, prefix="/api/admin/financial", tags=["SaaS - Financial Reports"])
app.include_router(admin_ai.router, prefix="/api/admin/ai", tags=["Admin - Intelligence"])
app.include_router(admin_history.router, prefix="/api/admin", tags=["Admin - History"]) 
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Inbound Webhooks"])
app.include_router(webhooks_ifood.router, prefix="/api/webhooks", tags=["Inbound Webhooks"])
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
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
        manager.disconnect(websocket, company_slug)
@app.get("/", include_in_schema=False)
def root():
    return {"message": "MesaFlow Enterprise API v3.3.7 🚀", "docs": "/docs"}

