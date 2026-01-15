# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 22:35:00
import os
import sys
import io
from pathlib import Path

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ENV_PATH = Path(".env")

def activate():
    print("🚀 Ativando Provedor Fiscal: Focus NFe (Modo Sandbox)...")
    
    if not ENV_PATH.exists():
        print("❌ Erro: Arquivo .env não encontrado.")
        return 1

    content = ENV_PATH.read_text(encoding="utf-8")
    
    # Configurações para ativação
    configs = {
        "FISCAL_PROVIDER": "focus",
        "FISCAL_ENV": "sandbox",
        "FISCAL_PRODUCTION_CONFIRMED": "false"
    }

    new_lines = []
    existing_keys = set()
    
    for line in content.splitlines():
        if "=" in line and not line.startswith("#"):
            key = line.split("=")[0].strip()
            if key in configs:
                new_lines.append(f"{key}={configs[key]}")
                existing_keys.add(key)
                continue
        new_lines.append(line)

    # Adiciona chaves que não existiam
    for key, value in configs.items():
        if key not in existing_keys:
            new_lines.append(f"{key}={value}")

    ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    
    print("✅ Arquivo .env atualizado.")
    print("⚠️  Lembre-se de adicionar seu 'FISCAL_TOKEN' manualmente no .env.")
    return 0

if __name__ == "__main__":
    sys.exit(activate())
