
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 09:15:00
import os
import shutil
from pathlib import Path

def hard_reset():
    print("🧹 Iniciando Hard Reset do Ambiente Mobile...")
    
    # 1. Remover pastas de build nativo que causam o conflito 'Bare Workflow'
    # Se o objetivo é usar Expo Go, essas pastas não devem existir em dev
    folders_to_delete = ["mobile/android", "mobile/ios", "mobile/.expo"]
    
    for folder in folders_to_delete:
        path = Path(folder)
        if path.exists():
            print(f"   🗑️  Removendo {folder}...")
            shutil.rmtree(path)
            
    # 2. Limpar cache do Metro
    print("   🧼 Limpando cache do Metro Bundler...")
    # No Windows, o cache fica em pastas temporárias
    os.system("npx expo start --clear")

if __name__ == "__main__":
    hard_reset()

