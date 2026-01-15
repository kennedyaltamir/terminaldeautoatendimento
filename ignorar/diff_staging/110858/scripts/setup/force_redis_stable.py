# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:30:00
import os
import subprocess
import sys
import time

def stabilize_infra():
    print("🔧 Estabilizando Infraestrutura para Gold Master...")
    # 1. Limpa containers antigos
    subprocess.run("docker rm -f mesaflow-redis", shell=True, capture_output=True)
    # 2. Sobe Redis limpo
    subprocess.run("docker run -d -p 6379:6379 --name mesaflow-redis redis:alpine", shell=True, check=True)
    print("✅ Redis reiniciado.")
    
    # 3. Patch no .env para usar IP direto (evita latência de DNS no Windows)
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            content = f.read()
        new_content = content.replace("localhost:6379", "127.0.0.1:6379")
        with open(env_path, "w") as f:
            f.write(new_content)
        print("✅ .env atualizado para 127.0.0.1")

if __name__ == "__main__":
    stabilize_infra()
