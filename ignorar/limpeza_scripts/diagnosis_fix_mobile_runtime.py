# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:15:00
import os
import json
from pathlib import Path

def fix():
    print("🔧 MesaFlow Mobile Runtime Fixer")
    print("================================")

    app_json_path = Path("mobile/app.json")
    
    if not app_json_path.exists():
        print("❌ Erro: mobile/app.json nao encontrado.")
        return

    try:
        with open(app_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Correcao da Runtime Version para Bare Workflow
        print("🛠️  Ajustando runtimeVersion para string estatica")
        data['expo']['runtimeVersion'] = "1.0.0"
        
        # Garante que nao existam politicas conflitantes
        if 'updates' in data['expo'] and 'fallbackToCacheTimeout' not in data['expo']['updates']:
            data['expo']['updates']['fallbackToCacheTimeout'] = 0

        with open(app_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print("✅ mobile/app.json atualizado com sucesso.")

        print("\n🚀 COMANDOS PARA EXECUTAR AGORA:")
        print("1. cd mobile")
        print("2. npx expo start --clear")
        print("3. Pressione 'a' para abrir no Android")
        print("\nSe o erro persistir, tente forçar o modo tunnel:")
        print("   npx expo start --tunnel")
        
    except Exception as e:
        print(f"❌ Falha ao processar arquivo: {e}")

if __name__ == "__main__":
    fix()
