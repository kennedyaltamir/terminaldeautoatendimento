import json
import os
import sys

def fix_package_json():
    print("🔧 Reparando mobile/package.json...")
    
    # Caminho absoluto para garantir que o script encontre o arquivo
    # Assume que o script é rodado da raiz do projeto
    file_path = os.path.join(os.getcwd(), "mobile", "package.json")
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        sys.exit(1)
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Garante que a seção scripts existe
        if "scripts" not in data:
            data["scripts"] = {}
            
        # Injeta ou atualiza o script de teste
        if "test" not in data["scripts"]:
            print("   ➕ Adicionando script 'test': 'jest'")
            data["scripts"]["test"] = "jest"
            
            # Salva o arquivo
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("✅ mobile/package.json corrigido com sucesso.")
        else:
            print(f"   ℹ️  Script 'test' já existe: {data['scripts']['test']}")
            
    except Exception as e:
        print(f"❌ Erro ao processar JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_package_json()
