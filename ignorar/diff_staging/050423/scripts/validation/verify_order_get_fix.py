# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 05:15:00
import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_order_get():
    print("🔍 Verificando endpoint público de consulta de pedido...")
    try:
        # 1. Tenta buscar um pedido inexistente para validar a ROTA (deve dar 404, não 405 ou 404 de rota)
        # Usamos um UUID aleatório
        fake_id = "00000000-0000-0000-0000-000000000000"
        res = requests.get(f"{BASE_URL}/orders/{fake_id}", timeout=5)
        
        if res.status_code == 404:
            # Se o corpo contiver "Pedido não encontrado", a rota existe e a lógica funcionou
            data = res.json()
            if data.get("detail") == "Pedido não encontrado":
                print("✅ SUCESSO: Endpoint /api/orders/{id} operacional.")
                return True
            else:
                print(f"❌ FALHA: Resposta inesperada: {data}")
                return False
        else:
            print(f"❌ FALHA: Status inesperado: {res.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 ERRO DE CONEXÃO: {e}")
        return False

if __name__ == "__main__":
    if test_order_get():
        sys.exit(0)
    else:
        sys.exit(1)
