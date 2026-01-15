
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 04:10:00
import os
import sys
from pathlib import Path

def check_mobile_readiness():
    print("🔍 Iniciando Mobile Production Gate...")
    mobile_dir = Path("mobile")
    
    # 1. Check Hardcoded IPs
    env_file = mobile_dir / "src" / "config" / "env.ts"
    if env_file.exists():
        content = env_file.read_text()
        if "192.168." in content or "localhost" in content:
            print("🚨 BLOQUEADOR: IP de desenvolvimento detectado em env.ts")
            return False

    # 2. Check Assets Size
    icon = mobile_dir / "assets" / "icon.png"
    if icon.exists() and icon.stat().st_size < 500:
        print("⚠️ AVISO: Ícones do app parecem ser placeholders (tamanho muito pequeno).")

    # 3. Check Package Name
    app_json = mobile_dir / "app.json"
    if app_json.exists():
        import json
        data = json.load(open(app_json))
        pkg = data.get("expo", {}).get("android", {}).get("package", "")
        if "com.example" in pkg or not pkg:
            print("🚨 BLOQUEADOR: Package name inválido em app.json")
            return False

    print("✅ Mobile Gate: Configurações básicas validadas.")
    return True

if __name__ == "__main__":
    if not check_mobile_readiness():
        sys.exit(1)

