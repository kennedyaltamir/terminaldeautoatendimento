# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-16 11:05:00
import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🧹 OPS-01: COGNITIVE PRUNE (L10 Hygiene)
# ==============================================================================
# Objetivo: Isolar ruído cognitivo (logs, reports antigos, temporários).
# Destino: ignorar/prune_archive/<timestamp>/
# ==============================================================================

def run_prune():
    print("🧹 Iniciando Podagem Cognitiva (Higiene L10)...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_base = Path("ignorar/prune_archive") / timestamp
    
    # Padrões de arquivos/pastas que são considerados "ruído"
    noise_patterns = [
        "comunication/logs",
        "testesvisuais/run_*",
        "atualizar.log",
        "structure_audit.txt",
        "todos_markdowns.txt",
        "resposta.txt"
    ]
    
    moved_count = 0
    
    for pattern in noise_patterns:
        # Lida com caminhos diretos e globs
        path_obj = Path(".")
        for item in path_obj.glob(pattern):
            if item.exists() and "ignorar" not in str(item):
                dest = archive_base / item.relative_to(".")
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.move(str(item), str(dest))
                    print(f"   [➔] Isolado: {item}")
                    moved_count += 1
                except Exception as e:
                    print(f"   [!] Erro ao mover {item}: {e}")

    print(f"\n✨ Podagem concluída. {moved_count} itens movidos para {archive_base}")
    return 0

if __name__ == "__main__":
    run_prune()

