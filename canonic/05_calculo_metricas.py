# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 10:26:00
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Metricas")

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    if not results_path.exists(): return

    with open(results_path, "r") as f: results = json.load(f)
        
    total = len(results)
    criticals = [s for s in results if s.get("is_critical")]
    
    avg_score = sum(s.get("score", 0) for s in results) / total if total > 0 else 0
    
    # Cobertura Ponderada (Críticos valem 4x)
    weighted_sum = 0
    total_weight = 0
    for s in results:
        weight = 4 if s.get("is_critical") else 1
        weighted_sum += (s.get("score", 0) * weight)
        total_weight += (100 * weight)
        
    coverage = (weighted_sum / total_weight * 100) if total_weight > 0 else 0
    
    # Contagem de sucessos críticos para o relatório
    critical_ok = len([s for s in criticals if s.get("score", 0) >= 80])
    
    metrics = {
        "total_screens": total,
        "avg_score": round(avg_score, 2),
        "weighted_coverage": round(coverage, 2),
        "critical_total": len(criticals),
        "critical_ok": critical_ok,
        "ci_gate": "PASS" if coverage >= 50 and critical_ok > 0 else "FAIL",
        "critical_blockers": len(criticals) - critical_ok
    }
    
    with open("docs/audit/ui_audit_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
        
    logger.info(f"Métricas: Cobertura {metrics['weighted_coverage']}% | Críticos OK: {critical_ok}/{len(criticals)}")

if __name__ == "__main__":
    run()

