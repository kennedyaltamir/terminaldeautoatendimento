# DOMAIN: DEVOPS_SCRIPTS
import sys
import os
import json

def verify():
    print("🔍 Verificando TASK-GTM-09: Mobile OTA Updates (Strict Check)...")

    # 1. Verificar dependência no package.json
    pkg_path = "mobile/package.json"
    if not os.path.exists(pkg_path):
        print("❌ mobile/package.json não encontrado.")
        sys.exit(1)

    try:
        with open(pkg_path, "r", encoding="utf-8") as f:
            pkg = json.load(f)
            if "expo-updates" not in pkg.get("dependencies", {}):
                print("❌ Dependência 'expo-updates' ausente no package.json.")
                sys.exit(1)
            print("✅ Dependência 'expo-updates' encontrada.")
    except Exception as e:
        print(f"❌ Erro ao ler package.json: {e}")
        sys.exit(1)

    # 2. Verificar configuração no app.json
    app_path = "mobile/app.json"
    if not os.path.exists(app_path):
        print("❌ mobile/app.json não encontrado.")
        sys.exit(1)

    try:
        with open(app_path, "r", encoding="utf-8") as f:
            app_config = json.load(f)
            expo = app_config.get("expo", {})
            
            updates = expo.get("updates", {})
            if not updates.get("enabled"):
                print("❌ Updates não habilitados em app.json.")
                sys.exit(1)
            
            if "u.expo.dev" not in updates.get("url", ""):
                print("❌ URL de updates inválida ou ausente.")
                sys.exit(1)

            runtime = expo.get("runtimeVersion", {})
            if runtime.get("policy") != "appVersion":
                print("❌ Política de runtimeVersion incorreta (esperado: appVersion).")
                sys.exit(1)
                
            print("✅ Configuração de Updates no app.json validada.")
    except Exception as e:
        print(f"❌ Erro ao ler app.json: {e}")
        sys.exit(1)

    # 3. Verificar canais no eas.json
    eas_path = "mobile/eas.json"
    if not os.path.exists(eas_path):
        print("❌ mobile/eas.json não encontrado.")
        sys.exit(1)

    try:
        with open(eas_path, "r", encoding="utf-8") as f:
            eas = json.load(f)
            builds = eas.get("build", {})
            
            if builds.get("preview", {}).get("channel") != "preview":
                print("❌ Canal 'preview' não configurado corretamente.")
                sys.exit(1)
                
            if builds.get("production", {}).get("channel") != "production":
                print("❌ Canal 'production' não configurado corretamente.")
                sys.exit(1)
                
            print("✅ Canais de Release no eas.json validados.")
    except Exception as e:
        print(f"❌ Erro ao ler eas.json: {e}")
        sys.exit(1)

    print("\n🏆 TASK-GTM-09: VALIDAÇÃO CONCLUÍDA.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
