import os
import sys
import json

# [TEST_EXEMPT: Script de pré-validação de build nativo]

def verify_pre_build():
    print("🔍 Iniciando Smoke Test de Pré-Build (Missão 36)...")

    errors = 0
    
    # 1. Verificar se o projeto está configurado para o EAS
    app_json_path = "mobile/app.json"
    with open(app_json_path, "r") as f:
        data = json.load(f).get("expo", {})
        if "extra" in data and "eas" in data["extra"]:
            print("✅ app.json: Project ID do EAS configurado.")
        else:
            print("❌ app.json: extra.eas.projectId ausente. Rode 'eas project:init'.")
            errors += 1

    # 2. Verificar se existem variáveis de ambiente para o build
    # O build nativo exige que a API_URL esteja definida
    env_path = "mobile/.env" # Ou variáveis no EAS Dashboard
    if not os.path.exists(env_path):
        print("⚠️  AVISO: mobile/.env não encontrado. Certifique-se de configurar as Secrets no painel da Expo.")

    # 3. Verificar integridade dos Assets (Ícones e Splash)
    assets = [
        "mobile/assets/icon.png",
        "mobile/assets/splash.png",
        "mobile/assets/adaptive-icon.png"
    ]
    for asset in assets:
        if os.path.exists(asset):
            print(f"✅ Asset encontrado: {asset}")
        else:
            print(f"❌ Asset FALTANDO: {asset}")
            errors += 1

    print("\n" + "="*50)
    if errors == 0:
        print("✨ PRONTO PARA BUILD: O ambiente mobile está estável para compilação.")
        sys.exit(0)
    else:
        print(f"🚨 BLOQUEIO: Corrija os {errors} erros antes de gastar créditos de build.")
        sys.exit(1)

if __name__ == "__main__":
    verify_pre_build()
