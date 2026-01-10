# DOMAIN: DEVOPS_SCRIPTS
import sys
import os
from fastapi.routing import APIRoute

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.main import app

def list_routes():
    print("🔍 Listando rotas registradas no FastAPI...")
    
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ", ".join(route.methods)
            routes.append(f"{methods} {route.path}")
        else:
            # WebSocket ou Mount (Static Files)
            routes.append(f"WEBSOCKET/MOUNT {route.path}")
            
    routes.sort()
    
    print(f"📊 Total de rotas: {len(routes)}")
    print("-" * 50)
    for r in routes:
        print(r)
    print("-" * 50)
    
    # Verificação específica
    target = "service-requests"
    found = any(target in r for r in routes)
    
    if found:
        print(f"✅ Rota de Service Requests ENCONTRADA na lista.")
    else:
        print(f"❌ Rota de Service Requests NÃO ENCONTRADA.")
        print("   Possível causa: O arquivo app/routers/admin.py não foi salvo ou o servidor não reiniciou.")

if __name__ == "__main__":
    list_routes()
