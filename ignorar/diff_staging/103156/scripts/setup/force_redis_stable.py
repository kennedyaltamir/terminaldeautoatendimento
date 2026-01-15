# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 13:30:00
import os
from pathlib import Path

def fix_redis_config():
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env não encontrado.")
        return
    
    content = env_path.read_text(encoding="utf-8")
    # Força o uso de IP para evitar problemas de resolução 'localhost' no Windows
    new_content = content.replace("localhost:6379", "127.0.0.1:6379")
    
    if "REDIS_URL" not in new_content:
        new_content += "\nREDIS_URL=redis://127.0.0.1:6379/0\n"
        
    env_path.write_text(new_content, encoding="utf-8")
    print("✅ Configuração de Redis otimizada para 127.0.0.1 (Estabilidade Windows).")

if __name__ == "__main__":
    fix_redis_config()
