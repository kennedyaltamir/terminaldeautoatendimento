import sys
import os
import json

def verify():
    print("🔍 Verificando TASK-040: Configuração OTA Updates...")
    
    # 1. Verificação de Arquivos
    required_files = [
        "mobile/app.json",
        "mobile/eas.json",
        "mobile/package.json"
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
            updates = app_config.get("expo", {}).get("updates", {})
            runtime = app_config.get("expo", {}).get("runtimeVersion", {})
            
            if not updates.get("enabled"):
                print("❌ Updates desabilitados em app.json")
                sys.exit(1)
            
            if updates.get("url") != "https://u.expo.dev/6c399079-8815-4995-ad7d-7b23c6fa1769":
                print("❌ URL de updates incorreta ou ausente.")
                sys.exit(1)

            if runtime.get("policy") != "appVersion":
                print("❌ Política de runtimeVersion incorreta (esperado: appVersion).")
                sys.exit(1)
                
            print("✅ app.json validado (Updates & RuntimeVersion).")
    except Exception as e:
        print(f"❌ Erro ao ler app.json: {e}")
        sys.exit(1)

    # 3. Validação de eas.json
    try:
        with open("mobile/eas.json", "r", encoding="utf-8") as f:
            eas_config = json.load(f)
            
            preview_channel = eas_config["build"]["preview"].get("channel")
            prod_channel = eas_config["build"]["production"].get("channel")
            
            if preview_channel != "preview":
                print("❌ Canal 'preview' não configurado no perfil preview.")
                sys.exit(1)
                
            if prod_channel != "production":
                print("❌ Canal 'production' não configurado no perfil production.")
                sys.exit(1)
                
            print("✅ eas.json validado (Channels).")
    except Exception as e:
        print(f"❌ Erro ao ler eas.json: {e}")
        sys.exit(1)

    # 4. Validação de package.json (Dependência)
    try:
        with open("mobile/package.json", "r", encoding="utf-8") as f:
            pkg = json.load(f)
            if "expo-updates" not in pkg.get("dependencies", {}):
                print("❌ Dependência 'expo-updates' não encontrada no package.json.")
                print("   👉 Execute: python scripts/setup/setup_ota.py")
                sys.exit(1)
            print("✅ Dependência 'expo-updates' confirmada.")
    except Exception as e:
        print(f"❌ Erro ao ler package.json: {e}")
        sys.exit(1)

    print("\n🏆 TASK-040: OTA UPDATES CONFIGURADO COM SUCESSO.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
