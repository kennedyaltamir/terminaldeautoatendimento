import requests
import sys
import time

# Configuração
BASE_URL = "http://localhost:8000/api"

def verify_revocation():
    print("🔍 Verificando TASK-SEC-04: Revogação de JWT...")

    # 0. Verificar se o Backend está com Redis ativo para este teste
    try:
        health_res = requests.get("http://localhost:8000/health", timeout=2)
        health_data = health_res.json()
        if health_data.get("services", {}).get("redis") != "up":
            print("❌ ERRO: O serviço Redis está offline no Backend.")
            print("   O teste de revogação SEMPRE falhará sem um Redis funcional.")
            print("   DICA: Inicie o Redis localmente ou configure REDIS_URL.")
            sys.exit(1)
    except Exception:
        pass # Deixa seguir para o erro de conexão se o backend estiver totalmente off

    # 1. Login para obter token
    print("🔑 Realizando login de teste...")
    try:
        auth_res = requests.post(
            f"{BASE_URL}/auth/token", 
            data={"username": "admin@mesaflow.com", "password": "123456"}
        )
        if auth_res.status_code != 200:
            print(f"❌ Falha no login: {auth_res.text}")
            sys.exit(1)
        
        data = auth_res.json()
        token = data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Token obtido.")

    except Exception as e:
        print(f"❌ Erro de conexão com o servidor: {e}")
        sys.exit(1)

    # 2. Testar acesso com token válido
    print("📡 Testando acesso com token ativo...")
    res_valid = requests.get(f"{BASE_URL}/admin/metrics", headers=headers)
    if res_valid.status_code != 200:
        print(f"❌ Acesso negado com token válido: {res_valid.status_code}")
        sys.exit(1)
    print("✅ Acesso autorizado.")

    # 3. Executar Logout (Revogação)
    print("🚪 Executando Logout (Revogação)...")
    res_logout = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    if res_logout.status_code != 204:
        print(f"❌ Erro no logout: {res_logout.status_code}")
        sys.exit(1)
    print("✅ Logout concluído com sucesso.")

    # 4. Testar acesso com token revogado (Blacklist)
    print("🛡️  Testando acesso com token revogado...")
    # Delay para garantir processamento
    time.sleep(1)
    
    res_blocked = requests.get(f"{BASE_URL}/admin/metrics", headers=headers)
    
    if res_blocked.status_code == 401:
        print("✅ SUCESSO: Token bloqueado pela blacklist.")
        print("\n🏆 JWT Revocation Verified: Token blocked after logout.")
        sys.exit(0)
    else:
        print(f"❌ FALHA: O token revogado CONTINUA com acesso (Status {res_blocked.status_code}).")
        print("   CAUSA PROVÁVEL: O backend não conseguiu gravar/ler do Redis.")
        sys.exit(1)

if __name__ == "__main__":
    verify_revocation()
