# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 05:05:00
import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_dashboard_route():
    print("🔍 Verificando correção da rota /api/admin/tables/dashboard...")
    try:
        # Testamos sem token para verificar se a rota EXISTE (deve retornar 401, não 404)
        res = requests.get(f"{BASE_URL}/admin/tables/dashboard", timeout=5)
        
        if res.status_code == 401:
            print("✅ SUCESSO: Rota encontrada e protegida (401 Unauthorized).")
            return True
        elif res.status_code == 404:
            print("❌ FALHA: Rota ainda retorna 404 Not Found.")
            return False
        else:
            print(f"⚠️  AVISO: Status inesperado: {res.status_code}")
            return res.status_code < 500
    except Exception as e:
        print(f"💥 ERRO DE CONEXÃO: {e}")
        return False

if __name__ == "__main__":
    if test_dashboard_route():
        sys.exit(0)
    else:
        sys.exit(1)
