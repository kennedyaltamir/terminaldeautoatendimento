# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 10:46:00
import shutil
import os
from pathlib import Path

def cleanup():
    print("🧹 Executando Limpeza Final de Resíduos Legados...")
    
    targets = [
        "docs/governance",
        "comunication/scripts"
    ]
    
    ignore_dir = Path("ignorar/legacy_archive")
    ignore_dir.mkdir(parents=True, exist_ok=True)
    
    for target in targets:
        path = Path(target)
        if path.exists():
            dest = ignore_dir / path.name
            if dest.exists(): shutil.rmtree(dest)
            shutil.move(str(path), str(dest))
            print(f"   📦 Movido para ignorar: {target}")
            
    print("✨ Limpeza concluída. O sistema está purificado para o Gold Master.")

if __name__ == "__main__":
    cleanup()

