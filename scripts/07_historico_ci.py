# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 09:56:00
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("CI_History")

def run():
    metrics_path = Path("docs/audit/ui_audit_metrics.json")
    history_path = Path("docs/audit/ui_audit_history.json")
    
    if not metrics_path.exists(): return

    with open(metrics_path, "r") as f: metrics = json.load(f)
    
    history = []
    if history_path.exists():
        with open(history_path, "r") as f: history = json.load(f)
        
    entry = {
        "timestamp": datetime.now().isoformat(),
        "coverage": metrics["weighted_coverage"],
        "score": metrics["avg_score"],
        "gate": metrics["ci_gate"]
    }
    
    history.append(entry)
    # Mantém apenas os últimos 50 registros
    history = history[-50:]
    
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)
        
    # Gera arquivo simplificado para o GitHub Actions
    with open("docs/audit/ui_audit_ci.json", "w") as f:
        json.dump({"status": metrics["ci_gate"], "coverage": metrics["weighted_coverage"]}, f)
        
    logger.info(f"Histórico atualizado. Status CI: {metrics['ci_gate']}")

if __name__ == "__main__":
    run()

