import os
import sys
import json

# [TEST_EXEMPT: Script de auditoria de configuração de produção]

def verify():
    print("🔍 Iniciando Auditoria de Preparação para Produção (Missão 35)...")

    errors = 0
    
    # 1. Verificar eas.json
    eas_path = "mobile/eas.json"
    if not os.path.exists(eas_path):
        print("❌ FALTANDO: mobile/eas.json")
        errors += 1
    else:
        with open(eas_path, "r") as f:
            data = json.load(f)
            if "production" in data.get("build", {}):
                print("✅ eas.json: Perfil de produção configurado.")
            else:
                print("❌ eas.json: Perfil de produção ausente.")
                errors += 1

    # 2. Verificar app.json (Metadados de Loja)
    app_json_path = "mobile/app.json"
    with open(app_json_path, "r") as f:
        data = json.load(f).get("expo", {})
        
        # iOS
        if "bundleIdentifier" in data.get("ios", {}):
            print(f"✅ iOS: Bundle ID definido ({data['ios']['bundleIdentifier']})")
        else:
            print("❌ iOS: bundleIdentifier ausente.")
            errors += 1
            
        # Android
        if "package" in data.get("android", {}):
            print(f"✅ Android: Package definido ({data['android']['package']})")
        else:
            print("❌ Android: package ausente.")
            errors += 1

    print("\n" + "="*50)
    if errors == 0:
        print("✨ SUCESSO: O aplicativo está configurado para build de produção.")
        sys.exit(0)
    else:
        print(f"🚨 ALERTA: {errors} pendência(s) de configuração encontradas.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
