import requests
import sys
import time

def check_production(api_url):
    """
    Verifica se o deploy em produção foi bem sucedido com tolerância a Cold Start.
    """
    print(f"🚀 Iniciando Verificação Pós-Deploy (Modo Resiliente): {api_url}")
    
    # Render Free + Neon podem levar tempo para acordar (Cold Start)
    # Aumentamos para 60s para garantir a subida inicial
    MAX_RETRIES = 3
    TIMEOUT = 60 

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"📡 Tentativa {attempt}/{MAX_RETRIES}...")
            start_time = time.time()
            
            # 1. Testar Root
            res_root = requests.get(api_url, timeout=TIMEOUT)
            latency = (time.time() - start_time) * 1000
            
            if res_root.status_code == 200:
                print(f"✅ API Online ({latency:.2f}ms): {res_root.json().get('message')}")
            
                # 2. Testar Sinais Vitais (Health)
                res_health = requests.get(f"{api_url}/api/health", timeout=TIMEOUT)
                if res_health.status_code == 200:
                    data = res_health.json()
                    print(f"✅ Sinais Vitais: {data['status'].upper()}")
                    print(f"   - Database: {data['services']['database']}")
                    print(f"   - Redis: {data['services']['redis']}")
                    return True
                else:
                    print(f"⚠️  Root OK, mas Health Check falhou (Status {res_health.status_code})")
                    return False
            else:
                print(f"❌ Erro: API retornou status {res_root.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"⏳ Timeout na tentativa {attempt}. O servidor está acordando...")
            if attempt < MAX_RETRIES:
                time.sleep(5) # Espera 5s antes de tentar de novo
            continue
        except Exception as e:
            print(f"🔥 Falha Crítica: {e}")
            return False

    print("❌ Falha: O servidor não respondeu após múltiplas tentativas.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python post_deploy_check.py https://sua-api.onrender.com")
        sys.exit(1)
    
    success = check_production(sys.argv[1])
    sys.exit(0 if success else 1)
