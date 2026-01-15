# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 13:55:00
import os
import sys
import subprocess
import time
from pathlib import Path

# Tenta importar redis, instala se necessário para garantir execução do guardião
try:
    import redis
except ImportError:
    print("📦 Instalando dependência 'redis' para o guardião de infraestrutura...")
    subprocess.run([sys.executable, "-m", "pip", "install", "redis"], stdout=subprocess.DEVNULL)
    import redis

ENV_PATH = Path(".env")

def check_redis_alive(url):
    """Verifica se o Redis está aceitando conexões e respondendo PONG."""
    try:
        r = redis.from_url(url, socket_connect_timeout=1)
        return r.ping()
    except Exception:
        return False

def main():
    print("========================================")
    print("🔧 MESAFLOW INFRASTRUCTURE GUARD")
    print("========================================")
    
    # No Windows, 127.0.0.1 é mais estável que 'localhost' para drivers async
    target_url = "redis://127.0.0.1:6379/0"
    
    if check_redis_alive(target_url):
        print("✅ Redis está ONLINE e respondendo.")
        sys.exit(0)
    
    print("❌ Redis OFFLINE. Tentando subir via Docker...")
    
    # Tenta remover container zumbi se existir
    subprocess.run(
        "docker rm -f mesaflow-redis",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    # Tenta subir o container oficial
    try:
        subprocess.run(
            "docker run -d -p 6379:6379 --name mesaflow-redis --restart always redis:alpine",
            shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("🚨 ERRO: Falha ao executar comando Docker. O Docker Desktop está aberto?")
        sys.exit(1)
    
    # Aguarda estabilização do serviço (Boot do Alpine + Redis)
    for i in range(5):
        sys.stdout.write(f"\r⏳ Aguardando boot do serviço... ({i+1}/5)")
        sys.stdout.flush()
        time.sleep(1)
        if check_redis_alive(target_url):
            print("\n✨ Redis recuperado com sucesso!")
            sys.exit(0)
            
    print("\n🚨 FALHA CRÍTICA: O container subiu, mas o Redis não respondeu no tempo limite.")
    print("O sistema não pode operar em modo Gold Master sem broker de eventos.")
    sys.exit(1)

if __name__ == "__main__":
    main()
