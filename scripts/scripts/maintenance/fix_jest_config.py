import subprocess
import os
import sys

def fix_jest():
    print("🔧 Reparando configuração do Jest para React Native Testing Library...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    # 1. Remover configuração duplicada do package.json
    # O Jest não gosta de ter config no package.json E no jest.config.js
    print("🧹 Limpando configuração 'jest' do package.json...")
    try:
        import json
        pkg_path = os.path.join(mobile_dir, "package.json")
        with open(pkg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if "jest" in data:
            del data["jest"]
            with open(pkg_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("✅ Configuração removida do package.json.")
        else:
            print("ℹ️  Nenhuma configuração 'jest' encontrada no package.json.")

    except Exception as e:
        print(f"❌ Erro ao limpar package.json: {e}")

    print("✅ Jest Config reparado.")

if __name__ == "__main__":
    fix_jest()
