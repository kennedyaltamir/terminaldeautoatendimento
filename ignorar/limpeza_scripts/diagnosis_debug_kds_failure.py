# DOMAIN: DEVOPS_SCRIPTS
import requests
import sys
import json

# Configuração
BASE_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def debug_kds():
    print(f"🕵️ INICIANDO DIAGNÓSTICO DE FALHA NO KDS...\n")

    # 1. Autenticação
    print("1️⃣  Testando Autenticação...")
    try:
        auth_res = requests.post(f"{BASE_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS})
        if auth_res.status_code != 200:
            print(f"{Colors.RED}❌ Falha no login: {auth_res.text}{Colors.ENDC}")
            return
        token = auth_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print(f"{Colors.GREEN}✅ Login OK.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ Erro de conexão: {e}{Colors.ENDC}")
        return

    # 2. Teste da Rota de Pedidos (Principal)
    print("\n2️⃣  Testando Rota de Pedidos (/orders)...")
    orders_url = f"{BASE_URL}/admin/{SLUG}/orders"
    orders_res = requests.get(orders_url, headers=headers)
    
    if orders_res.status_code == 200:
        orders = orders_res.json()
        count = len(orders)
        print(f"{Colors.GREEN}✅ Rota /orders respondeu 200 OK.{Colors.ENDC}")
        print(f"   📦 Pedidos encontrados: {count}")
        
        if count > 0:
            # Analisa o primeiro pedido para ver se tem a estação correta
            first = orders[0]
            print(f"   📝 Exemplo de Pedido: ID={first['id'][:6]} Status={first['status']}")
            if 'items' in first and len(first['items']) > 0:
                station = first['items'][0]['product'].get('station')
                print(f"   🍳 Estação do Produto: {station}")
                if station != 'kitchen':
                    print(f"{Colors.YELLOW}⚠️  AVISO: A estação é '{station}'. O filtro padrão do KDS é 'kitchen'.{Colors.ENDC}")
    else:
        print(f"{Colors.RED}❌ Rota /orders falhou: {orders_res.status_code}{Colors.ENDC}")

    # 3. Teste da Rota de Chamados (Suspeita de Causa Raiz)
    print("\n3️⃣  Testando Rota de Chamados (/service-requests)...")
    requests_url = f"{BASE_URL}/admin/{SLUG}/service-requests"
    req_res = requests.get(requests_url, headers=headers)

    if req_res.status_code == 200:
        print(f"{Colors.GREEN}✅ Rota /service-requests respondeu 200 OK.{Colors.ENDC}")
    elif req_res.status_code == 404:
        print(f"{Colors.RED}❌ Rota /service-requests retornou 404 NOT FOUND.{Colors.ENDC}")
        print(f"{Colors.RED}🚨 DIAGNÓSTICO CONFIRMADO: A falta desta rota está quebrando o Promise.all no Frontend.{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}⚠️  Rota /service-requests retornou {req_res.status_code}.{Colors.ENDC}")

if __name__ == "__main__":
    debug_kds()
