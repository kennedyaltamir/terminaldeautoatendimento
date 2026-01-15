
import os
import sys
import shutil
import subprocess
from pathlib import Path

# Configuração
MOBILE_DIR = Path("mobile")
ENV_FILE = MOBILE_DIR / ".env"
REQUIRED_VARS = ["EXPO_PUBLIC_API_URL", "EXPO_PUBLIC_WS_URL"]

def check_node_version():
    print("🔍 Verificando Node.js...")
    try:
        result = subprocess.run(["node", "-v"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"   ✅ Node.js detectado: {version}")
        # Expo 50+ recomenda Node 18+
        major = int(version.replace("v", "").split(".")[0])
        if major < 18:
            print("   ❌ ERRO: Node.js 18+ é necessário para Expo SDK 50+.")
            return False
        return True
    except FileNotFoundError:
        print("   ❌ ERRO: Node.js não encontrado no PATH.")
        return False

def check_adb():
    print("🔍 Verificando Android Debug Bridge (ADB)...")
    if shutil.which("adb"):
        print("   ✅ ADB detectado no PATH.")
        return True
    else:
        print("   ⚠️  AVISO: ADB não encontrado. O emulador pode não iniciar automaticamente.")
        # Não falha o build, pois pode ser iOS ou Web, mas avisa.
        return True

def check_env_vars():
    print("🔍 Verificando Variáveis de Ambiente (Local)...")
    if not ENV_FILE.exists():
        print(f"   ❌ ERRO: Arquivo {ENV_FILE} não encontrado.")
        print("      Ação: Crie o arquivo .env na pasta mobile/ com EXPO_PUBLIC_API_URL.")
        return False
    
    content = ENV_FILE.read_text(encoding="utf-8")
    missing = []
    for var in REQUIRED_VARS:
        if var not in content:
            missing.append(var)
    
    if missing:
        print(f"   ❌ ERRO: Variáveis ausentes no .env: {', '.join(missing)}")
        return False
    
    print("   ✅ Variáveis de ambiente validadas.")
    return True

def check_dependencies():
    print("🔍 Verificando Dependências (node_modules)...")
    if not (MOBILE_DIR / "node_modules").exists():
        print("   ⚠️  node_modules não encontrado. Instalação será necessária.")
        return True # O script de run vai instalar
    print("   ✅ node_modules presente.")
    return True

def main():
    print("========================================")
    print("📱 MOBILE BUILD AUDIT (PRE-FLIGHT)")
    print("========================================")
    
    if not MOBILE_DIR.exists():
        print("❌ ERRO CRÍTICO: Pasta 'mobile/' não encontrada na raiz.")
        sys.exit(1)

    checks = [
        check_node_version(),
        check_adb(),
        check_env_vars(),
        check_dependencies()
    ]

    if all(checks):
        print("\n✅ AMBIENTE MOBILE PRONTO PARA EXECUÇÃO.")
        sys.exit(0)
    else:
        print("\n❌ FALHA NA AUDITORIA. CORRIJA OS ERROS ACIMA.")
        sys.exit(1)

if __name__ == "__main__":
    main()

