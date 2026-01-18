
import os
from pathlib import Path

MOBILE_DIR = Path("mobile")
ENV_FILE = MOBILE_DIR / ".env"
APP_FILE = MOBILE_DIR / "App.tsx"

def verify_telemetry():
    print("📡 Verificando Telemetria (Sentry)...")
    
    # 1. Verificar Dependência
    package_json = (MOBILE_DIR / "package.json").read_text()
    if "@sentry/react-native" not in package_json:
        print("❌ ERRO: @sentry/react-native não encontrado no package.json")
        return False
    print("   ✅ Dependência instalada.")

    # 2. Verificar Inicialização no App.tsx
    app_content = APP_FILE.read_text()
    if "initSentry()" not in app_content:
        print("❌ ERRO: initSentry() não chamado no App.tsx")
        return False
    print("   ✅ Inicialização detectada no App.tsx.")

    # 3. Verificar Variável de Ambiente
    if not ENV_FILE.exists():
        print("⚠️  AVISO: .env não encontrado. Certifique-se de configurar EXPO_PUBLIC_SENTRY_DSN no EAS.")
    else:
        env_content = ENV_FILE.read_text()
        if "EXPO_PUBLIC_SENTRY_DSN" not in env_content:
            print("❌ ERRO: EXPO_PUBLIC_SENTRY_DSN ausente no .env local.")
            return False
        print("   ✅ Variável de ambiente configurada.")

    print("\n✨ Telemetria Validada (Static Check).")
    return True

if __name__ == "__main__":
    if verify_telemetry():
        exit(0)
    else:
        exit(1)

