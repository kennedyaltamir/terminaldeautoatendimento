# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 17:15:00
import os
import sys
import time
from pathlib import Path

# Tenta importar redis
try:
    import redis
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "redis"], stdout=subprocess.DEVNULL)
    import redis

ENV_PATH = Path(".env")

def patch_env_force():
    print("📝 Forçando configuração do .env para 127.0.0.1...")
    
    if not ENV_PATH.exists():
        print("   ❌ .env não encontrado.")
        return False

    content = ENV_PATH.read_text(encoding="utf-8")
    new_lines = []
    target_url = "redis://127.0.0.1:6379/0"
    patched = False
    
    for line in content.splitlines():
        if line.startswith("REDIS_URL="):
            new_lines.append(f"REDIS_URL={target_url}")
            patched = True
        else:
            new_lines.append(line)
            
    if not patched:
        new_lines.append(f"REDIS_URL={target_url}")

    ENV_PATH.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"   ✅ .env atualizado.")
    return True

def test_connection():
    print("🔌 Testando conexão direta com Redis (Bypass Docker Check)...")
    try:
        # Timeout curto para não travar
        r = redis.from_url("redis://127.0.0.1:6379/0", socket_connect_timeout=3)
        if r.ping():
            print("   ✨ SUCESSO: Redis conectado e respondendo PONG!")
            return True
    except Exception as e:
        print(f"   ❌ Falha na conexão: {e}")
        print("      Dica: Verifique se o container 'mesaflow-redis' está verde no Docker Desktop.")
        return False

if __name__ == "__main__":
    if patch_env_force():
        if test_connection():
            print("\n🚀 Tudo pronto! O Redis está configurado.")
            print("   Agora você pode rodar 'python run.py' e os WebSockets funcionarão.")
        else:
            print("\n⚠️  Configuração aplicada, mas o Redis não respondeu.")
