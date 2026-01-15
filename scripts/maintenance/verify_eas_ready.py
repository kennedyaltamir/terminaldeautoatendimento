
import subprocess
import sys
import json
import os
from pathlib import Path

MOBILE_DIR = Path("mobile")
EAS_JSON = MOBILE_DIR / "eas.json"
APP_JSON = MOBILE_DIR / "app.json"

def check_command(cmd):
    try:
        # shell=True necessário no Windows para resolver PATH do npm/npx
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def verify_eas():
    print("☁️  MESAFLOW EAS READINESS CHECK")
    print("================================")

    # 1. Arquivos
    if not EAS_JSON.exists():
        print("❌ ERRO: eas.json não encontrado.")
        return False
    print("✅ eas.json presente.")

    # 2. CLI Instalada
    if not check_command("eas --version"):
        print("❌ ERRO: EAS CLI não instalada. Rode 'npm install -g eas-cli'.")
        return False
    print("✅ EAS CLI detectada.")

    # 3. Login (Opcional em CI se usar token, obrigatório local)
    if "EXPO_TOKEN" not in os.environ:
        print("🔍 Verificando login local...")
        try:
            result = subprocess.run("eas whoami", shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print("⚠️  AVISO: Não logado no EAS. Rode 'eas login' antes do build.")
            else:
                print(f"✅ Logado como: {result.stdout.strip()}")
        except:
            print("⚠️  Não foi possível verificar login EAS.")
    else:
        print("✅ EXPO_TOKEN detectado no ambiente (CI Mode).")

    # 4. Project ID
    try:
        with open(APP_JSON, 'r', encoding='utf-8') as f:
            app_config = json.load(f)
            project_id = app_config.get('expo', {}).get('extra', {}).get('eas', {}).get('projectId')
            if not project_id:
                print("⚠️  AVISO: projectId não encontrado em app.json. O primeiro build irá configurá-lo.")
            else:
                print(f"✅ Project ID configurado: {project_id}")
    except Exception as e:
        print(f"❌ Erro ao ler app.json: {e}")
        return False

    print("\n✨ EAS READY: Ambiente pronto para Build & Submit.")
    return True

if __name__ == "__main__":
    if verify_eas():
        sys.exit(0)
    else:
        sys.exit(1)

