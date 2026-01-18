import os
import re
from pathlib import Path

# ==============================================================================
# 🗺️ FRONTEND ROUTE DISCOVERER
# ==============================================================================
# Objetivo: Mapear todas as rotas do Next.js (App Router) baseadas em arquivos page.tsx
# ==============================================================================

FRONTEND_ROOT = Path("frontend/src/app")

# Valores padrão para rotas dinâmicas
MOCK_PARAMS = {
    "[slug]": "hamburgueria-ze",
    "[tableId]": "1",
    "[orderId]": "mock-order-id",
    "[categoryId]": "1",
    "[productId]": "1"
}

def discover_routes():
    print(f"🚀 Mapeando rotas em: {FRONTEND_ROOT}")
    
    routes = []
    
    for root, dirs, files in os.walk(FRONTEND_ROOT):
        if "page.tsx" in files:
            # 1. Obter caminho relativo
            rel_path = Path(root).relative_to(FRONTEND_ROOT)
            path_str = str(rel_path).replace("\\", "/")
            
            # 2. Limpar Grupos de Rota do Next.js (ex: (auth))
            # Remove pastas que começam com ( e terminam com )
            parts = [p for p in path_str.split("/") if not (p.startswith("(") and p.endswith(")"))]
            clean_path = "/".join(parts)
            
            # 3. Tratar rota raiz
            if clean_path == ".":
                route = "/"
            else:
                route = "/" + clean_path
            
            # 4. Gerar URL de Teste (Substituindo [params])
            test_url = route
            for param, value in MOCK_PARAMS.items():
                test_url = test_url.replace(param, value)
            
            routes.append({
                "file": str(Path(root) / "page.tsx"),
                "route": route,
                "test_url": test_url
            })

    # Ordenar por URL
    routes.sort(key=lambda x: x["route"])
    
    print(f"\n✅ Encontradas {len(routes)} telas:\n")
    
    print(f"{'ROTA (Next.js)':<40} | {'URL DE TESTE':<40}")
    print("-" * 85)
    
    for r in routes:
        print(f"{r['route']:<40} | {r['test_url']:<40}")

    return routes

if __name__ == "__main__":
    discover_routes()

