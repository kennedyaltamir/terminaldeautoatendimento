
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 04:10:00
import requests
import time
import concurrent.futures

BASE_URL = "http://localhost:8000/api"
TOKEN_TENANT_A = "TOKEN_VALIDO_A" # Deve ser preenchido para teste real
ID_PEDIDO_TENANT_B = "ID_DE_OUTRA_EMPRESA"

def test_rls_breach():
    print("🛡️ Testando tentativa de vazamento Cross-Tenant (RLS)...")
    headers = {"Authorization": f"Bearer {TOKEN_TENANT_A}"}
    # Tenta acessar pedido que não pertence ao Tenant A
    res = requests.get(f"{BASE_URL}/admin/orders/{ID_PEDIDO_TENANT_B}", headers=headers)
    if res.status_code == 404:
        print("   ✅ SUCESSO: RLS bloqueou o acesso (404 Not Found).")
    else:
        print(f"   🚨 FALHA: Acesso indevido permitido ou erro inesperado: {res.status_code}")

def test_ai_concurrency_stress():
    print("🧠 Testando estresse de concorrência na IA (RFC-011)...")
    headers = {"Authorization": f"Bearer {TOKEN_TENANT_A}"}
    
    def call_ai():
        return requests.get(f"{BASE_URL}/admin/ai/forecast?days=30", headers=headers)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(call_ai) for _ in range(20)]
        results = [f.result().status_code for f in futures]
    
    success = results.count(200)
    throttled = results.count(429) # Se houver rate limit
    print(f"   📊 Resultados: {success} Sucessos, {throttled} Throttled.")

if __name__ == "__main__":
    # test_rls_breach()
    # test_ai_concurrency_stress()
    print("Script pronto. Requer tokens reais para execução.")

