import requests
import sys

def check_production(api_url):
    """
    Verifica se o deploy em produção foi bem sucedido.
    """
    print(f"🚀 Iniciando Verificação Pós-Deploy: {api_url}")
    
    try:
        # 1. Testar Root
        res_root = requests.get(api_url, timeout=10)
        if res_root.status_code == 200:
            print(f"✅ API Online: {res_root.json().get('message')}")
        
        # 2. Testar Sinais Vitais (Health)
        res_health = requests.get(f"{api_url}/api/health", timeout=10)
        if res_health.status_code == 200:
            data = res_health.json()
            print(f"✅ Sinais Vitais: {data['status'].upper()}")
            print(f"   - Database: {data['services']['database']}")
            print(f"   - Redis: {data['services']['redis']}")
            
        return True
    except Exception as e:
        print(f"❌ Erro ao validar produção: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python post_deploy_check.py https://sua-api.onrender.com")
        sys.exit(1)
    
    success = check_production(sys.argv[1])
    sys.exit(0 if success else 1)
