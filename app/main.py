from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import public, admin, auth, admin_menu, admin_company, admin_tables, admin_metrics, payments, webhooks, admin_inventory, admin_employees
from app.websockets import manager

app = FastAPI(
    title="MesaFlow API",
    description="API de Autoatendimento para Restaurantes",
    version="0.1.0"
)

# Configuração de CORS para permitir acesso da rede Wi-Fi
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.150:3000", # Seu IP Local
    "*" # Libera geral para a demo funcionar sem erro de bloqueio
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas HTTP
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(public.router, prefix="/api", tags=["Public"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin Orders"])
app.include_router(admin_menu.router, prefix="/api/admin/menu", tags=["Admin Menu"])
app.include_router(admin_company.router, prefix="/api/admin/company", tags=["Admin Company"])
app.include_router(admin_tables.router, prefix="/api/admin/tables", tags=["Admin Tables"])
app.include_router(admin_metrics.router, prefix="/api/admin/metrics", tags=["Admin Metrics"])
app.include_router(admin_inventory.router, prefix="/api/admin/inventory", tags=["Admin Inventory"])
app.include_router(admin_employees.router, prefix="/api/admin/employees", tags=["Admin Employees"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])

# Rota WebSocket
@app.websocket("/ws/{company_slug}")
async def websocket_endpoint(websocket: WebSocket, company_slug: str):
    await manager.connect(websocket, company_slug)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, company_slug)
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
        manager.disconnect(websocket, company_slug)

@app.get("/")
def root():
    return {"message": "MesaFlow API is running 🚀"}