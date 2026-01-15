import sys
import os
import json

def verify():
    print("🔍 Verificando TASK-036: Configuração de Build Nativo...")
    
    # 1. Verificação de Arquivos de Configuração
    required_files = [
        "mobile/app.json",
        "mobile/eas.json"
    ]
    
    for f_path in required_files:
        if not os.path.exists(f_path):
            print(f"❌ Arquivo faltando: {f_path}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f_path}")

    # 2. Validação de app.json
    try:
        with open("mobile/app.json", "r", encoding="utf-8") as f:
            app_config = json.load(f)
            android_config = app_config.get("expo", {}).get("android", {})
            
            if android_config.get("package") != "com.mesaflow.mobile":
                print("❌ Package name incorreto em app.json")
                sys.exit(1)
            
            if "versionCode" not in android_config:
                print("❌ versionCode ausente em app.json")
                sys.exit(1)
                
            print("✅ app.json validado (Package & VersionCode).")
    except Exception as e:
        print(f"❌ Erro ao ler app.json: {e}")
        sys.exit(1)

    # 3. Validação de eas.json
    try:
        with open("mobile/eas.json", "r", encoding="utf-8") as f:
            eas_config = json.load(f)
            
            if "production" not in eas_config.get("build", {}):
                print("❌ Perfil 'production' ausente em eas.json")
                sys.exit(1)
                
            prod_env = eas_config["build"]["production"].get("env", {})
            if prod_env.get("NPM_CONFIG_LEGACY_PEER_DEPS") != "true":
                print("❌ Configuração de legacy-peer-deps ausente no perfil de produção.")
                sys.exit(1)
                
            print("✅ eas.json validado (Profiles & Env).")
    except Exception as e:
        print(f"❌ Erro ao ler eas.json: {e}")
        sys.exit(1)

    print("\n🏆 TASK-036: CONFIGURAÇÃO DE BUILD VALIDADA.")
    print("👉 Para gerar o APK, execute: cd mobile && eas build --platform android --profile preview --local")
    sys.exit(0)

if __name__ == "__main__":
    verify()
