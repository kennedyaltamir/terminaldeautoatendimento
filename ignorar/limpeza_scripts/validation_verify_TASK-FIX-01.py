# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-09 18:10:00
import requests
import sys
import uuid

# Configuração
BASE_URL = "http://localhost:8000/api"

def verify_fix():
    print("🔍 Verificando TASK-FIX-01: Correção de 404 em Listas Vazias...")

    # 1. Setup: Criar empresa nova (sem dados)
    unique_id = uuid.uuid4().hex[:6]
    slug = f"fix-404-{unique_id}"
    email = f"fix-{unique_id}@test.com"
    password = "Password123!"

    print("🏗️  Criando empresa de teste...")
    res_reg = requests.post(f"{BASE_URL}/auth/register", json={
        "company_name": f"Fix Corp {unique_id}",
        "company_slug": slug,
        "owner_email": email,
        "password": password,
        "segment": "gastro"
    })

    if res_reg.status_code != 201:
        print(f"❌ Falha no registro: {res_reg.text}")
        sys.exit(1)

    token = res_reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Teste: Service Requests (Lista Vazia)
    print("🧪 Teste 1: GET /service-requests (Vazio)...")
    res_req = requests.get(f"{BASE_URL}/admin/{slug}/service-requests", headers=headers)

    if res_req.status_code == 200:
        data = res_req.json()
        if isinstance(data, list) and len(data) == 0:
            print("✅ Sucesso: Retornou 200 OK e lista vazia []")
        else:
            print(f"❌ Falha: Retornou 200 mas payload incorreto: {data}")
            sys.exit(1)
    elif res_req.status_code == 404:
        print("❌ FALHA CRÍTICA: Retornou 404 Not Found (Bug persiste).")
        sys.exit(1)
    else:
        print(f"❌ Falha: Status inesperado {res_req.status_code}")
        sys.exit(1)

    # 3. Teste: Orders (Lista Vazia)
    print("🧪 Teste 2: GET /orders (Vazio)...")
    res_ord = requests.get(f"{BASE_URL}/admin/{slug}/orders", headers=headers)

    if res_ord.status_code == 200:
        data = res_ord.json()
        if isinstance(data, list) and len(data) == 0:
            print("✅ Sucesso: Retornou 200 OK e lista vazia []")
        else:
            print(f"❌ Falha: Retornou 200 mas payload incorreto: {data}")
            sys.exit(1)
    elif res_ord.status_code == 404:
        print("❌ FALHA CRÍTICA: Retornou 404 Not Found (Bug persiste).")
        sys.exit(1)
    else:
        print(f"❌ Falha: Status inesperado {res_ord.status_code}")
        sys.exit(1)

    print("\n🏆 TASK-FIX-01: VALIDAÇÃO CONCLUÍDA. O KDS ESTÁ SEGURO.")
    sys.exit(0)

if __name__ == "__main__":
    verify_fix()