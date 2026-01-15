
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 09:00:00
import os

ENV_FILE = ".env"
SECRET_KEY = "IFOOD_WEBHOOK_SECRET"
DEFAULT_VALUE = "default_secret_change_me"

def patch_env():
    print(f"🔧 Patching {ENV_FILE} com {SECRET_KEY}...")
    
    if not os.path.exists(ENV_FILE):
        print(f"❌ Arquivo {ENV_FILE} não encontrado.")
        return

    with open(ENV_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if SECRET_KEY in content:
        print(f"✅ {SECRET_KEY} já existe no .env. Nenhuma alteração necessária.")
    else:
        with open(ENV_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n# Integração iFood (Compliance-Grade)\n{SECRET_KEY}={DEFAULT_VALUE}\n")
        print(f"✅ {SECRET_KEY} adicionado com sucesso.")

if __name__ == "__main__":
    patch_env()

