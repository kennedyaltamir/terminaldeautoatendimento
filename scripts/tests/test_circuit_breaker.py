# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 01:55:00
import requests
import time
import sys
BASE_URL = "http://localhost:8000/api"
def check_api_online():
    try:
        requests.get(f"{BASE_URL.replace('/api', '')}/health", timeout=2)
        return True
    except:
        return False
def simulate_failure_storm():
    if not check_api_online():
        print("❌ ERRO: A API não está rodando na porta 8000. Inicie com 'python run.py' primeiro.")
        sys.exit(1)
    print("🌪️  Iniciando tempestade de erros simulada (Threshold: 20 erros)...")
    for i in range(1, 25):
        try:
            # Usamos uma rota pública inexistente para gerar 404 sem precisar de token
            res = requests.get(f"{BASE_URL}/public/non-existent-trigger", timeout=0.5)
            sys.stdout.write(f"\r   🚀 Requisição {i}/24 - Status: {res.status_code}")
        except:
            sys.stdout.write(f"\r   🚀 Requisição {i}/24 - Timeout/Erro")
        sys.stdout.flush()
        time.sleep(0.05)
    print("\n✅ Tempestade enviada.")
def verify_breaker():
    print("🔍 Verificando estado do Circuit Breaker...")
    try:
        res = requests.get(f"{BASE_URL}/resolve-domain?host=test", timeout=1)
        if res.status_code == 503:
            print(f"✨ SUCESSO: Circuito ABERTO (Status 503).")
            return True
        else:
            print(f"❌ FALHA: Circuito continua FECHADO (Status: {res.status_code})")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar: {e}")
        return False
if __name__ == "__main__":
    simulate_failure_storm()
    time.sleep(1)
    if verify_breaker():
        print("\n🏆 SLO ENFORCEMENT VALIDADO.")
    else:
        sys.exit(1)
