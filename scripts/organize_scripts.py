import os
import shutil
from pathlib import Path

# Configuração de Pastas e Padrões
STRUCTURE = {
    "security": [
        "audit", "security", "auth", "create_admin", "fix_layouts"
    ],
    "functional": [
        "logistics", "payment", "delivery", "stock", "order", "menu", 
        "kds", "waiter", "franchise", "marketing", "simular", "test_"
    ],
    "maintenance": [
        "update_db", "fix_db", "seed", "cleanup", "purge", "fix_deps", 
        "fix_fiscal", "fix_tips", "fix_pwa", "fix_sentry"
    ],
    "setup": [
        "check_env", "verify", "download", "install", "configurar", "gerar_url"
    ]
}

# Arquivos que devem permanecer na raiz de scripts/ (Utilitários gerais)
KEEP_IN_ROOT = ["organize_scripts.py", "__init__.py"]

def organize():
    base_dir = Path("scripts")
    
    if not base_dir.exists():
        print("❌ Pasta 'scripts' não encontrada.")
        return

    # 1. Criar subpastas
    for folder in STRUCTURE.keys():
        (base_dir / folder).mkdir(exist_ok=True)
        print(f"📁 Pasta verificada: scripts/{folder}")

    # 2. Mover arquivos
    moved_count = 0
    for file in base_dir.iterdir():
        if file.is_dir() or file.name in KEEP_IN_ROOT:
            continue

        filename = file.name.lower()
        target_folder = None

        # Lógica de Classificação
        for folder, keywords in STRUCTURE.items():
            if any(k in filename for k in keywords):
                target_folder = folder
                break
        
        # Se não casou com nada, move para 'maintenance' por padrão se for .py
        if not target_folder and file.suffix == ".py":
            target_folder = "maintenance"

        if target_folder:
            target_path = base_dir / target_folder / file.name
            try:
                shutil.move(str(file), str(target_path))
                print(f"✅ Movido: {file.name} -> {target_folder}/")
                moved_count += 1
            except Exception as e:
                print(f"❌ Erro ao mover {file.name}: {e}")

    print(f"\n✨ Organização concluída! {moved_count} scripts movidos.")

if __name__ == "__main__":
    organize()
