# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 09:58:00
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Alertas")

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    if not results_path.exists(): return

    with open(results_path, "r") as f: results = json.load(f)
    
    logger.info("=== MATRIZ DE PRIORIDADE ===")
    
    for s in results:
        msg = f"{s['normalized_name']} ({s['platform']}) - Score: {s['score']}%"
        
        if s["is_critical"] and s["status"] != "VALID":
            logger.warning(f"🔴 CRÍTICO: {msg}")
        elif s["status"] == "DRAFT":
            logger.info(f"🟡 MÉDIA: {msg}")
        elif s["status"] == "VALID":
            logger.info(f"🟢 BAIXA: {msg}")

if __name__ == "__main__":
    run()

