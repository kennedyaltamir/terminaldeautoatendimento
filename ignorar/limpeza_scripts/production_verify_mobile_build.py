# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 19:35:00
import json
import os
import sys

def verify_mobile_config():
    print("🔍 Iniciando Verificação de Configuração de Build Mobile (GTM)...")

    # Caminhos
    eas_path = os.path.join("mobile", "eas.json")
    app_path = os.path.join("mobile", "app.json")

    # 1. Verificar existência dos arquivos
    if not os.path.exists(eas_path):
        print(f"❌ Arquivo não encontrado: {eas_path}")
        sys.exit(1)
    
    if not os.path.exists(app_path):
        print(f"❌ Arquivo não encontrado: {app_path}")
        sys.exit(1)

    # 2. Validar eas.json (Perfil de Produção)
    try:
        with open(eas_path, "r", encoding="utf-8") as f:
            eas_config = json.load(f)
        
        prod_config = eas_config.get("build", {}).get("production", {})
        
        if not prod_config:
            print("❌ Perfil 'production' não encontrado em eas.json")
            sys.exit(1)

        # Android: App Bundle
        if prod_config.get("android", {}).get("buildType") != "app-bundle":
            print("❌ Android production buildType deve ser 'app-bundle' para Google Play.")
            sys.exit(1)

        # iOS: Store Distribution
        if prod_config.get("ios", {}).get("distribution") != "store":
            print("❌ iOS production distribution deve ser 'store' para App Store.")
            sys.exit(1)

        # Env Vars
        if prod_config.get("env", {}).get("APP_ENV") != "production":
            print("❌ Variável APP_ENV deve ser 'production'.")
            sys.exit(1)

        print("✅ eas.json validado com sucesso.")

    except json.JSONDecodeError:
        print("❌ Erro de sintaxe no eas.json")
        sys.exit(1)

    # 3. Validar app.json (Identificadores)
    try:
        with open(app_path, "r", encoding="utf-8") as f:
            app_config = json.load(f).get("expo", {})

        # Android Package
        android_pkg = app_config.get("android", {}).get("package")
        if not android_pkg or android_pkg == "com.example.app":
            print(f"❌ Android package inválido ou padrão: {android_pkg}")
            sys.exit(1)

        # iOS Bundle ID
        ios_bundle = app_config.get("ios", {}).get("bundleIdentifier")
        if not ios_bundle or ios_bundle == "com.example.app":
            print(f"❌ iOS bundleIdentifier inválido ou padrão: {ios_bundle}")
            sys.exit(1)

        # Versionamento
        if not app_config.get("version"):
            print("❌ Versão do app não definida.")
            sys.exit(1)

        print(f"✅ app.json validado. Package: {android_pkg} | Version: {app_config.get('version')}")

    except json.JSONDecodeError:
        print("❌ Erro de sintaxe no app.json")
        sys.exit(1)

    print("\n🏆 Mobile Build Config Verified: READY FOR STORE SUBMISSION.")
    sys.exit(0)

if __name__ == "__main__":
    verify_mobile_config()