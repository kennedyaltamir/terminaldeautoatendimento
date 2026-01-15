import os
import sys

# [TEST_EXEMPT: Script de validação estrutural de infraestrutura de navegação]

def verify():
    print("🔍 Verificando Infraestrutura de Navegação Mobile (v1.1)...")
    
    critical_files = [
        "mobile/src/navigation/RootNavigator.tsx",
        "mobile/src/navigation/AuthStack.tsx",
        "mobile/src/navigation/AppStack.tsx"
    ]
    
    errors = 0
    
    # 1. Verificar existência de arquivos
    for f in critical_files:
        if not os.path.exists(f):
            print(f"❌ Arquivo ausente: {f}")
            errors += 1
        else:
            print(f"✅ Encontrado: {f}")

    # 2. Verificar App.tsx (Busca flexível por componentes chave)
    app_path = "mobile/App.tsx"
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_container = "NavigationContainer" in content
            has_navigator = "RootNavigator" in content
            
            if not has_container or not has_navigator:
                print(f"❌ App.tsx incompleto. Container: {has_container}, Navigator: {has_navigator}")
                errors += 1
            else:
                print(f"✅ App.tsx validado.")

    # 3. Verificar uso único de hydrate()
    print("🛡️ Verificando integridade do ciclo de hidratação...")
    hydrate_calls = []
    for root, _, files in os.walk("mobile/src"):
        for file in files:
            if file.endswith(".tsx") or file.endswith(".ts"):
                path = os.path.join(root, file).replace("\\", "/")
                with open(path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    # Ignora a definição da função na store e foca em chamadas de execução
                    if "hydrate()" in file_content and "auth.store" not in path:
                        hydrate_calls.append(path)
    
    if len(hydrate_calls) != 1 or "RootNavigator.tsx" not in hydrate_calls[0]:
        print(f"❌ VIOLAÇÃO: Chamada hydrate() deve existir apenas no RootNavigator. Encontrado em: {hydrate_calls}")
        errors += 1
    else:
        print("✅ Ciclo de hidratação isolado corretamente no RootNavigator.")

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s) encontrado(s).")
        sys.exit(1)
    
    print("\n✨ Mobile Navigation setup verified successfully.")

if __name__ == "__main__":
    verify()
