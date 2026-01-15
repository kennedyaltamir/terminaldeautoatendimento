# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 15:25:00
import redis
import os
from dotenv import load_dotenv

load_dotenv()

def validate():
    print("🔍 Validando integridade do Redis")
    
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    try:
        client = redis.from_url(redis_url, socket_connect_timeout=2)
        client.ping()
        print(f"✅ Conexao com Redis ({redis_url}): OK")
        
        # Teste de escrita/leitura
        client.set("mesaflow_test_key", "integrity_ok", ex=10)
        val = client.get("mesaflow_test_key")
        
        if val == b"integrity_ok" or val == "integrity_ok":
            print("✅ Teste de Escrita/Leitura: OK")
            exit(0)
        else:
            print(f"❌ ERRO: Valor recuperado incorreto: {val}")
            exit(1)
            
    except Exception as e:
        print(f"❌ FALHA: Nao foi possivel conectar ao Redis: {e}")
        exit(1)

if __name__ == "__main__":
    validate()
