
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 15:30:00
import os
import sys
import io
import requests
import inspect
from pathlib import Path
from fastapi.routing import APIRoute

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Adiciona raiz ao path para importar o app
sys.path.append(os.getcwd())

try:
    from app.main import app
except ImportError:
    print("❌ Erro crítico: Não foi possível importar 'app.main'. Verifique o PYTHONPATH.")
    sys.exit(1)

# Configuração
BASE_API_URL = "http://localhost:8000"
BASE_WEB_URL = "http://localhost:3000"
REPORT_PATH = "governance/evidence/REPORT_FULL_COVERAGE.md"
SLUG = "hamburgueria-ze"

def get_admin_token():
    try:
        res = requests.post(f"{BASE_API_URL}/api/auth/token", data={
            "username": "admin@mesaflow.com",
            "password": "123456"
        })
        if res.status_code == 200:
            return res.json()["access_token"]
    except:
        return None
    return None

def scan_backend_routes(token):
    print("🔍 Escaneando Rotas do Backend (FastAPI)...")
    routes = []
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ", ".join(route.methods)
            path = route.path
            
            # Tenta preencher parâmetros dinâmicos conhecidos para teste
            test_url = path.replace("{company_slug}", SLUG).replace("{slug}", SLUG)
            
            # Se ainda tiver chaves {}, é um parâmetro desconhecido (ex: {order_id})
            is_testable = "{" not in test_url and "GET" in route.methods
            
            status = "SKIPPED (Param)"
            status_code = "-"
            
            if is_testable:
                try:
                    res = requests.get(f"{BASE_API_URL}{test_url}", headers=headers, timeout=2)
                    status_code = res.status_code
                    if res.status_code in [200, 201]:
                        status = "✅ OK"
                    elif res.status_code in [401, 403]:
                        status = "🔒 AUTH"
                    else:
                        status = f"⚠️ {res.status_code}"
                except Exception as e:
                    status = "❌ ERROR"
            
            routes.append({
                "type": "API",
                "path": path,
                "methods": methods,
                "test_url": test_url if is_testable else "-",
                "status": status,
                "code": status_code
            })
            print(f"   [{methods}] {path:<50} -> {status}")
            
    return routes

def scan_frontend_pages():
    print("\n🔍 Escaneando Rotas do Frontend (Next.js)...")
    pages_dir = Path("frontend/src/app")
    routes = []
    
    for path in pages_dir.rglob("page.tsx"):
        # Converte caminho de arquivo para rota URL
        rel_path = path.relative_to(pages_dir)
        route_path = "/" + str(rel_path.parent).replace("\\", "/")
        
        # Limpeza de rotas dinâmicas e grupos
        route_path = route_path.replace("/.", "") # Raiz
        if route_path == "/": route_path = ""
        
        # Substitui slugs dinâmicos para teste
        test_url = route_path.replace("[slug]", SLUG)
        
        # Verifica se a página responde (SSR Check)
        status = "UNKNOWN"
        code = "-"
        try:
            res = requests.get(f"{BASE_WEB_URL}{test_url}", timeout=2)
            code = res.status_code
            if code == 200:
                status = "✅ RENDER"
            else:
                status = f"⚠️ {code}"
        except:
            status = "❌ OFFLINE"

        routes.append({
            "type": "WEB",
            "path": route_path or "/",
            "methods": "PAGE",
            "test_url": test_url,
            "status": status,
            "code": code
        })
        print(f"   [PAGE] {route_path or '/'} -> {status}")

    return routes

def generate_report(api_routes, web_routes):
    print(f"\n📝 Gerando Relatório: {REPORT_PATH}")
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    
    total = len(api_routes) + len(web_routes)
    success = len([r for r in api_routes + web_routes if "✅" in r["status"]])
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"# 👁️ Relatório de Omnisciência Sistêmica\n")
        f.write(f"**Cobertura Total:** {total} Rotas Mapeadas\n")
        f.write(f"**Taxa de Sucesso (Smoke Test):** {success}/{total} ({(success/total)*100:.1f}%)\n\n")
        
        f.write("## 1. Backend API (FastAPI)\n")
        f.write("| Método | Rota (Path) | Status | Código |\n")
        f.write("| :--- | :--- | :---: | :---: |\n")
        for r in api_routes:
            f.write(f"| {r['methods']} | `{r['path']}` | {r['status']} | {r['code']} |\n")
            
        f.write("\n## 2. Frontend Web (Next.js)\n")
        f.write("| Tipo | Rota (File) | URL Testada | Status |\n")
        f.write("| :--- | :--- | :--- | :---: |\n")
        for r in web_routes:
            f.write(f"| {r['methods']} | `{r['path']}` | `{r['test_url']}` | {r['status']} |\n")

    print("✅ Relatório gerado com sucesso.")

def main():
    print("====================================================")
    print("🚀 MESAFLOW OMNISCIENCE PROBE v1.0")
    print("   Mapeamento e Teste de Fumaça de Todas as Rotas")
    print("====================================================")
    
    token = get_admin_token()
    if not token:
        print("⚠️  Aviso: Não foi possível autenticar como Admin. Testes protegidos falharão (401).")
    else:
        print("🔑 Token Admin obtido. Executando testes autenticados.")
        
    api_routes = scan_backend_routes(token)
    web_routes = scan_frontend_pages()
    
    generate_report(api_routes, web_routes)

if __name__ == "__main__":
    main()

