# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 10:40:00
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Melhoria")

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    if not results_path.exists(): return

    with open(results_path, "r") as f: results = json.load(f)
    
    # Inteligência de Próximo Passo
    gaps = [s for s in results if s["is_critical"] and s["score"] < 80]
    gaps.sort(key=lambda x: x["score"])
    
    print("\n" + "="*60)
    print("🧠 INSIGHTS DE MELHORIA CONTÍNUA")
    print("="*60)
    
    if gaps:
        print(f"⚠️  Detectadas {len(gaps)} telas críticas com documentação insuficiente.")
        print("👉 Ação Recomendada: Priorize o preenchimento das seguintes telas:")
        for s in gaps[:3]:
            print(f"   - [{s['platform'].upper()}] {s['normalized_name']} (Score: {s['score']}%)")
    else:
        print("✅ Todas as telas críticas possuem documentação nota 80+.")
        print("🚀 O sistema está pronto para auditoria externa de conformidade.")
    
    print("-" * 60)
    logger.info("Pipeline de Auditoria Finalizado com Sucesso.")

if __name__ == "__main__":
    run()

