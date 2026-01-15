# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 13:55:00
import os
import sys
import subprocess
import time
from pathlib import Path

# Tenta importar redis
try:
    import redis
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "redis"], stdout=subprocess.DEVNULL)
    import redis

ENV_PATH = Path(".env")

def check_redis_alive(url):
    try:
        r = redis.from_url(url, socket_connect_timeout=1)
        return r.ping()
    except:
        return False

def main():
    print("========================================")
    print("🔧 MESAFLOW INFRASTRUCTURE GUARD")
    print("========================================")
    
    target_url = "redis://127.0.0.1:6379/0"
    
    if check_redis_alive(target_url):
        print("✅ Redis está ONLINE e respondendo.")
        sys.exit(0)
    
    print("❌ Redis OFFLINE. Tentando subir via Docker...")
    
    # Tenta subir o container
    subprocess.run(
        "docker run -d -p 6379:6379 --name mesaflow-redis --restart always redis:alpine",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    # Aguarda estabilização
    for i in range(5):
        sys.stdout.write(f"\r⏳ Aguardando boot... ({i+1}/5)")
        sys.stdout.flush()
        time.sleep(1)
        if check_redis_alive(target_url):
            print("\n✨ Redis recuperado com sucesso!")
            sys.exit(0)
            
    print("\n🚨 FALHA CRÍTICA: Não foi possível estabelecer conexão com o Redis.")
    print("O sistema não pode operar em modo Gold Master sem broker de eventos.")
    sys.exit(1)

if __name__ == "__main__":
    main()
