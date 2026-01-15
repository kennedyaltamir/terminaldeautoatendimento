# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 13:30:00
import os
from pathlib import Path

def fix_redis_config():
    env_path = Path(".env")
    if not env_path.exists(): return
    content = env_path.read_text()
    # Força IP em vez de hostname para evitar timeout no Windows
    new_content = content.replace("localhost:6379", "127.0.0.1:6379")
    env_path.write_text(new_content)
    print("✅ Configuração de Redis otimizada para 127.0.0.1")

if __name__ == "__main__":
    fix_redis_config()
