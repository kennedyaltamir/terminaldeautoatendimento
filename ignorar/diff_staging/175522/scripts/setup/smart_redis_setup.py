# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 17:00:00
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

def check_docker_running():
    try:
        # Verifica se o daemon do docker responde
        subprocess.run("docker ps", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def start_redis_container():
    container_name = "mesaflow-redis"
    print(f"   🚀 Subindo container '{container_name}'...")
    
    # Tenta remover container antigo/parado para garantir estado limpo
    subprocess.run(f"docker rm -f {container_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Roda novo container
    try:
        subprocess.run(
            f"docker run -d -p 6379:6379 --name {container_name} --restart always redis:alpine",
            shell=True, check=True, stdout=subprocess.DEVNULL
        )
        return True
    except Exception as e:
        print(f"   ❌ Erro ao subir container: {e}")
        return False

def patch_env(url):
    if not ENV_PATH.exists():
        print("   ❌ .env não encontrado.")
        return

    content = ENV_PATH.read_text(encoding="utf-8")
    new_lines = []
    patched = False
    
    for line in content.splitlines():
        if line.startswith("REDIS_URL="):
            new_lines.append(f"REDIS_URL={url}")
            patched = True
        else:
            new_lines.append(line)
    
    if not patched:
        new_lines.append(f"REDIS_URL={url}")

    ENV_PATH.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"   ✅ .env atualizado para: {url}")

def main():
    print("========================================")
    print("🔧 MESAFLOW SMART REDIS SETUP")
    print("========================================")

    if check_docker_running():
        print("✅ Docker detectado!")
        if start_redis_container():
            print("⏳ Aguardando boot do Redis (3s)...")
            time.sleep(3)
            # Usa 127.0.0.1 para evitar problemas de resolução de localhost no Windows
            patch_env("redis://127.0.0.1:6379/0")
            print("\n✨ SUCESSO: Redis Local Configurado.")
            print("👉 Reinicie o 'python run.py' para conectar.")
            return
    
    print("❌ Docker NÃO está rodando.")
    print("   Tentando aguardar você abrir o Docker Desktop...")
    
    max_retries = 10
    for i in range(max_retries):
        sys.stdout.write(f"\r⏳ Aguardando Docker... ({i+1}/{max_retries})")
        sys.stdout.flush()
        if check_docker_running():
            print("\n✅ Docker ficou online!")
            if start_redis_container():
                patch_env("redis://127.0.0.1:6379/0")
                print("\n✨ SUCESSO: Redis Local Configurado.")
                return
        time.sleep(3)

    print("\n\n⚠️  Tempo esgotado. O Docker não abriu.")
    print("   O sistema continuará funcionando, mas sem WebSockets (Real-time).")

if __name__ == "__main__":
    main()
