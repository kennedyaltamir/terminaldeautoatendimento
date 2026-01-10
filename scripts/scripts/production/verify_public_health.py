import requests
import sys

# Configuração
BASE_URL = "http://localhost:8000"

def verify_health_endpoints():
    print("🔍 Verificando Endpoints de Saúde (Dual Binding)...")

    endpoints = ["/health", "/api/health"]
    results = {}

    for endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                data = res.json()
                if "status" in data and "services" in data:
                    print(f"✅ {endpoint}: OK (Status: {data['status']})")
                    results[endpoint] = True
                else:
                    print(f"❌ {endpoint}: Payload inválido.")
                    results[endpoint] = False
            else:
                print(f"❌ {endpoint}: Status Code {res.status_code}")
                results[endpoint] = False
        except Exception as e:
            print(f"❌ {endpoint}: Erro de conexão ({e})")
            results[endpoint] = False

    if all(results.values()):
        print("\n🏆 Health Check Dual-Binding Verified: OK.")
        sys.exit(0)
    else:
        print("\n🚨 Falha na verificação de endpoints de saúde.")
        sys.exit(1)

if __name__ == "__main__":
    verify_health_endpoints()