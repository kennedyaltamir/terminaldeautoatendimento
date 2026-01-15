import os
import sys
import subprocess
import time
from pathlib import Path

# Tenta importar redis
try:
    import redis
except ImportError:
    print("📦 Instalando dependência 'redis'...")
    subprocess.run([sys.executable, "-m", "pip", "install", "redis"], stdout=subprocess.DEVNULL)
    import redis

def log(msg):
    print(f"[REDIS_GUARD] {msg}")

def check_redis_alive(url):
    try:
        r = redis.from_url(url, socket_connect_timeout=1)
        return r.ping()
    except Exception:
        return False

def main():
    log("🔧 Verificando Infraestrutura de Eventos...")
    
    # 127.0.0.1 é mandatório no Windows para evitar delay de DNS do localhost
    target_url = "redis://127.0.0.1:6379/0"
    
    if check_redis_alive(target_url):
        log("✅ Redis está ONLINE e respondendo.")
        sys.exit(0)

    log("❌ Redis OFFLINE. Tentando recuperação via Docker...")
    
    # Limpeza agressiva de containers zumbis
    subprocess.run("docker rm -f mesaflow-redis", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Start robusto
    try:
        log("🚀 Iniciando container 'mesaflow-redis'...")
        subprocess.run(
            "docker run -d -p 6379:6379 --name mesaflow-redis --restart always redis:alpine",
            shell=True, check=True, stdout=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        log("🚨 FALHA CRÍTICA: Docker não respondeu. Verifique se o Docker Desktop está aberto.")
        sys.exit(1)

    # Healthcheck loop
    for i in range(10):
        sys.stdout.write(f"\r⏳ Aguardando boot... ({i+1}/10)")
        sys.stdout.flush()
        time.sleep(1)
        if check_redis_alive(target_url):
            print("\n✅ Redis recuperado com sucesso!")
            
            # Patch no .env para garantir que o backend use o IP correto
            env_path = Path(".env")
            if env_path.exists():
                content = env_path.read_text(encoding="utf-8")
                if "localhost:6379" in content:
                    new_content = content.replace("localhost:6379", "127.0.0.1:6379")
                    env_path.write_text(new_content, encoding="utf-8")
                    log("📝 .env atualizado para 127.0.0.1")
            
            sys.exit(0)

    log("\n❌ Timeout: O container subiu mas não respondeu na porta 6379.")
    sys.exit(1)

if __name__ == "__main__":
    main()
