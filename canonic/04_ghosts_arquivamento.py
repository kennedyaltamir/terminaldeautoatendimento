# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 09:53:00
import json
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Ghosts")

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    archive_dir = Path("doctelas/_archive")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    if not results_path.exists(): return

    with open(results_path, "r") as f:
        results = json.load(f)
        
    # Identifica arquivos físicos que não estão no inventário (Ghosts)
    # Para este MVP, vamos focar em marcar os que falharam na normalização
    ghost_count = 0
    for screen in results:
        if screen["status"] == "MISSING":
            screen["is_ghost"] = False
            continue
            
        # Se o nome do arquivo for muito estranho ou duplicado, marcamos
        if len(screen["file_name"]) < 5:
            logger.warning(f"Possível Ghost detectado: {screen['file_name']}")
            screen["status"] = "GHOST"
            ghost_count += 1
            
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    logger.info(f"Processamento de Ghosts concluído. Detectados: {ghost_count}")

if __name__ == "__main__":
    run()

