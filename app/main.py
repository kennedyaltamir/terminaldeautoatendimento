# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-05 07:10:00
"""
//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 4.5.0 (CORS Hardened)
 * DNA_ID: MF-KERNEL-CORE-V4-5
 * OBJETIVO: Kernel Central de Orquestração do MesaFlow OS.
 * Comportamento esperado: 
 *  1. Orquestra o Ciclo de Vida (Lifespan) do servidor, WebSockets e Polling iFood.
 *  2. Gerencia a pilha de Middlewares: Rate Limiting -> CORS -> Circuit Breaker.
 *  3. Garante que erros sistêmicos (500/503) retornem headers CORS para leitura do Frontend.
 *  4. Registra integralmente a malha de roteamento administrativa e pública.
 */
//
"""
import os
import json
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# --- CORE INFRASTRUCTURE ---
from app.websockets import manager
from app.core.limiter import limiter
from app.core.config import settings
from app.core.logger import logger
from app.core.circuit_breaker import CircuitBreaker
from app.services.ifood_service import IfoodService

# --- ROUTER ARCHITECTURE ---
from app.routers import (
    auth_router, public_router, public_utils_router, upload_router,
    admin_router, admin_delivery_router, admin_logistics_router,
    admin_menu_router, admin_company_router, admin_tables_router,
    admin_metrics_router, admin_inventory_router, admin_employees_router,
    admin_billing_router, admin_payment_router, admin_audit_router,
    admin_fiscal_router, admin_financial_router, admin_marketing_router,
    admin_franchise_router, admin_integrations_router, admin_features_router,
    admin_ai_router, admin_history_router, payments_router,
    webhooks_router, webhooks_ifood_router, logistics_mobile_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Orquestrador de ritos de entrada e saída do Kernel."""
    # Startup: Inicializa malha de WebSockets e serviços de integração
    await manager.startup()
    ifood = IfoodService()
    asyncio.create_task(ifood.start_polling())
    yield
    # Shutdown: Encerramento gracioso de conexões persistentes
    await manager.shutdown()

# --- APP INITIALIZATION ---
app = FastAPI(
    title="MesaFlow API", 
    version="4.5.0", 
    description="Sistema Operacional Enterprise para Food Service",
    lifespan=lifespan
)

# --- RATE LIMITER CONFIG ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- MIDDLEWARE 1: CORS POLICY (PRIORIDADE ABSOLUTA) ---
# A ordem importa: CORS deve ser o primeiro middleware a processar a request
# para garantir que o browser receba os headers corretos mesmo em caso de erro 401/500.
origins = settings.BACKEND_CORS_ORIGINS
if settings.ENVIRONMENT == "development":
    # Em dev, permitimos wildcard se configurado, ou garantimos localhost
    if "*" not in origins:
        origins.append("http://localhost:3000")
        origins.append("http://127.0.0.1:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if settings.ENVIRONMENT != "development" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# --- MIDDLEWARE 2: RESILIÊNCIA E SEGURANÇA (CIRCUIT BREAKER) ---
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """
    Controlador de fluxo e resiliência.
    Garante integridade de transações e injeção de CORS em falhas fatais.
    """
    path = request.url.path
    
    # 🛡️ PROTOCOLO DE BYPASS: Infraestrutura e Autenticação ignoram o disjuntor
    # Isso evita que um travamento no banco bloqueie o login ou healthcheck
    is_infra = path.endswith(("/health", "/docs", "/openapi.json"))
    is_auth = "/api/auth/" in path
    
    if is_infra or is_auth:
        return await call_next(request)

    try:
        # 1. Health Check do Disjuntor (FSM do Sistema)
        await CircuitBreaker.check_health(request)
        
        # 2. Processamento da Request
        response = await call_next(request)
        
        # 3. Monitoramento de Sucesso (Filtro de Erros 5xx)
        if response.status_code >= 500:
            CircuitBreaker.record_error()
        else:
            CircuitBreaker.record_success()
            
        return response

    except Exception as e:
        # 4. Registro de Falha Sistêmica
        CircuitBreaker.record_error()
        logger.error(f"🚨 KERNEL_PANIC em {path}: {str(e)}")
        
        # 5. Rito de Resposta com Injeção Manual de CORS (Garante leitura no Frontend)
        # Mesmo que o middleware de CORS falhe ou seja ignorado por exceção não tratada,
        # garantimos os headers aqui.
        is_cb_open = "CIRCUIT_BREAKER_OPEN" in str(e)
        
        request_origin = request.headers.get("Origin", "*")
        
        return Response(
            content=json.dumps({
                "detail": str(e),
                "status": "CB_LOCKED" if is_cb_open else "INTERNAL_ERROR",
                "fix": "Execute reset_circuit_breaker.py em caso de falso-positivo."
            }),
            status_code=503 if is_cb_open else 500,
            media_type="application/json",
            headers={
                "Access-Control-Allow-Origin": request_origin,
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )

# --- ROUTER REGISTRATION ---
# Grupo 1: Identidade, Sessão e Mobile
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(logistics_mobile_router, prefix="/api/mobile/logistics", tags=["Logistics Mobile"])

# Grupo 2: Público, Upload e Utilitários
app.include_router(public_router, prefix="/api/public", tags=["Public API"])
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])
app.include_router(public_utils_router, prefix="/api/utils", tags=["Public Utils"])

# Grupo 3: Administração e Operação de Salão/Cozinha
app.include_router(admin_router, prefix="/api/admin", tags=["Admin Orders"])
app.include_router(admin_delivery_router, prefix="/api/admin/delivery", tags=["Admin Delivery"])
app.include_router(admin_logistics_router, prefix="/api/admin/logistics", tags=["Admin Logistics"])
app.include_router(admin_menu_router, prefix="/api/admin/menu", tags=["Admin Menu"])
app.include_router(admin_tables_router, prefix="/api/admin/tables", tags=["Admin Tables"])
app.include_router(admin_inventory_router, prefix="/api/admin/inventory", tags=["Admin Inventory"])
app.include_router(admin_company_router, prefix="/api/admin/company", tags=["Admin Company"])
app.include_router(admin_employees_router, prefix="/api/admin/employees", tags=["Admin Staff"])

# Grupo 4: Fintech, BI e Fiscal
app.include_router(admin_billing_router, prefix="/api/admin/billing", tags=["Admin Finance"])
app.include_router(admin_payment_router, prefix="/api/admin/payment", tags=["Admin Finance"])
app.include_router(admin_fiscal_router, prefix="/api/admin/fiscal", tags=["Admin Finance"])
app.include_router(admin_financial_router, prefix="/api/admin/financial", tags=["Admin Finance"])
app.include_router(admin_metrics_router, prefix="/api/admin/metrics", tags=["Admin Metrics"])
app.include_router(admin_ai_router, prefix="/api/admin/ai", tags=["Admin Intelligence"])
app.include_router(admin_history_router, prefix="/api/admin/history", tags=["Admin History"])

# Grupo 5: Governança, Integrações e Webhooks
app.include_router(admin_audit_router, prefix="/api/admin/audit", tags=["Admin Audit"])
app.include_router(admin_marketing_router, prefix="/api/admin/marketing", tags=["Admin Marketing"])
app.include_router(admin_franchise_router, prefix="/api/admin/franchise", tags=["Admin Franchise"])
app.include_router(admin_integrations_router, prefix="/api/admin/integrations", tags=["Admin System"])
app.include_router(admin_features_router, prefix="/api/admin/features", tags=["Admin System"])
app.include_router(webhooks_router, prefix="/api/webhooks", tags=["Integrations"])
app.include_router(webhooks_ifood_router, prefix="/api/webhooks/ifood", tags=["Integrations"])
app.include_router(payments_router, prefix="/api/payments", tags=["Integrations"])

# --- WEBSOCKET GATEWAY ---
@app.websocket("/api/ws/{slug}")
async def websocket_endpoint(websocket: WebSocket, slug: str):
    """Ponto de entrada de comunicação bi-direcional em tempo real."""
    await manager.connect(websocket, slug)
    try:
        while True:
            data = await websocket.receive_text()
            # Protocolo de Keep-Alive para infraestruturas Cloud
            if data == '{"type":"ping"}': 
                await websocket.send_text('{"type":"pong"}')
    except WebSocketDisconnect: 
        manager.disconnect(websocket, slug)
    except Exception: 
        manager.disconnect(websocket, slug)

# --- ROOT & HEALTHCHECK ---
@app.get("/api/health")
async def health(): 
    """Interface de diagnóstico de vitalidade."""
    return {"status": "healthy", "version": "4.5.0", "env": settings.ENVIRONMENT}

@app.get("/")
def root(): 
    """Interface de documentação rápida."""
    return {"message": "MesaFlow OS API v4.5.0 Online", "docs": "/docs"}