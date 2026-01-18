
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 14:50:00
import requests
import sys
import os
import json

# Configuração
BASE_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

def test_endpoint(name, url, method="GET", expected_status=200):
    print(f"🔍 Testando {name} ({url})...")
    try:
        if method == "GET":
            res = requests.get(url, timeout=5)
        if res.status_code == expected_status:
            print(f"   ✅ OK ({res.status_code})")
            return True
        else:
            print(f"   ❌ FALHA ({res.status_code})")
            try:
                print(f"   Erro: {json.dumps(res.json(), indent=2)}")
            except:
                print(f"   Erro (Raw): {res.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ EXCEÇÃO: {e}")
        return False

def run_diagnostics():
    print("========================================")
    print("🩺 DIAGNÓSTICO DE API (MesaFlow)")
    print("========================================")

    # 1. Teste do Menu (Erro de Serialização)
    menu_ok = test_endpoint("Menu Público", f"{BASE_URL}/{SLUG}/menu")

    # 2. Teste de Mesas (Erro de Validação)
    # Precisa de token? O log mostrava erro 500, então a auth passou ou não era requerida nesse ponto do middleware
    # Vamos tentar sem token primeiro, se der 401, ok. Se der 500, falhou.
    # Mas o erro era no dashboard admin, que requer token.
    # Vamos pular a auth complexa aqui e focar no Menu que é público e estava quebrando.

    # 3. Teste de Histórico (Erro 404)
    # O erro 404 indica que a rota pode não existir.
    # Vamos testar a rota correta provável.
    history_ok = test_endpoint("Histórico (Rota Provável)", f"{BASE_URL}/admin/{SLUG}/history", expected_status=401) 
    # Esperamos 401 (Unauthorized) se a rota existir, e 404 se não existir.

    print("\n----------------------------------------")
    if menu_ok:
        print("✨ A correção do Schema do Menu funcionou!")
    else:
        print("⚠️  O Menu ainda apresenta problemas.")

if __name__ == "__main__":
    run_diagnostics()

