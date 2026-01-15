import os
import shutil
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DE LIMPEZA DE SCRIPTS (Optimus v9 Context)
# ==============================================================================

SCRIPTS_DIR = Path("scripts/automation")
TRASH_DIR = Path("ignorar/obsoletos_automacao")

# Scripts que DEVEM permanecer (Ferramentas Atuais)
WHITELIST = {
    "optimus_v9_neuro_evolution.py", # O Cérebro Atual
    "map_routes.py",                 # Dependência Crítica
    "mapped_routes.json"             # Dependência Crítica
}

def cleanup_automation_scripts():
    print("🧹 Higienizando diretório de Automação (Optimus v9 Standard)...")
    
    if not TRASH_DIR.exists():
        TRASH_DIR.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    
    if SCRIPTS_DIR.exists():
        for file in SCRIPTS_DIR.iterdir():
            if file.is_file() and file.name not in WHITELIST:
                target_path = TRASH_DIR / file.name
                try:
                    shutil.move(str(file), str(target_path))
                    print(f"   🗑️  Arquivado: {file.name}")
                    moved_count += 1
                except Exception as e:
                    print(f"   ❌ Erro ao mover {file.name}: {e}")

    print(f"\n✨ Limpeza de Automação concluída. {moved_count} scripts arquivados.")
    print("   Apenas o Optimus v9 e suas dependências permanecem ativos.")

if __name__ == "__main__":
    cleanup_automation_scripts()
