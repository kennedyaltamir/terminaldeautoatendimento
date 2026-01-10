import sys
import os
import json

def verify():
    print("🔍 Verificando TASK-039: Deep Linking Universal...")
    
    # 1. Verificação de Arquivos
    required_files = [
        "mobile/app.json",
        "mobile/src/navigation/linking.ts",
        "mobile/App.tsx"
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
            expo_conf = app_config.get("expo", {})
            
            if expo_conf.get("scheme") != "mesaflow":
                print("❌ Scheme 'mesaflow' não configurado em app.json")
                sys.exit(1)
                
            android_conf = expo_conf.get("android", {})
            intent_filters = android_conf.get("intentFilters", [])
            has_scheme = any(
                f.get("data", [{}])[0].get("scheme") == "mesaflow" 
                for f in intent_filters
            )
            
            if not has_scheme:
                print("❌ Intent Filter para 'mesaflow' ausente no Android config.")
                sys.exit(1)
                
            print("✅ app.json validado (Scheme & IntentFilters).")
    except Exception as e:
        print(f"❌ Erro ao ler app.json: {e}")
        sys.exit(1)

    # 3. Validação de linking.ts
    with open("mobile/src/navigation/linking.ts", "r", encoding="utf-8") as f:
        content = f.read()
        if "mesaflow://" not in content:
            print("❌ Prefixo 'mesaflow://' não encontrado em linking.ts")
            sys.exit(1)
        if "OrderEntry" not in content:
            print("❌ Rota 'OrderEntry' não mapeada em linking.ts")
            sys.exit(1)

    # 4. Validação de App.tsx
    with open("mobile/App.tsx", "r", encoding="utf-8") as f:
        content = f.read()
        if "linking={linking}" not in content:
            print("❌ Propriedade 'linking' não injetada no NavigationContainer.")
            sys.exit(1)

    print("\n🏆 TASK-039: DEEP LINKING VALIDADO COM SUCESSO.")
    print("👉 Teste manual: npx uri-scheme open mesaflow://table/1 --android")
    sys.exit(0)

if __name__ == "__main__":
    verify()
