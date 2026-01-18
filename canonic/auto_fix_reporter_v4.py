
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 16:05:00
import os
import json
from pathlib import Path

# ==============================================================================
# 🛠️ AUTO FIX REPORTER v4 (Compliance Edition)
# ==============================================================================
# Consome os manifestos JSON (inda_summary.json) para criar o relatório executivo.
# ==============================================================================

OUTPUT_ROOT = Path("testesvisuais")

def generate_executive_report():
    print("🔍 Gerando Relatório Executivo (Compliance Grade)...")
    
    runs = sorted([d for d in OUTPUT_ROOT.glob("run_*") if d.is_dir()])
    if not runs:
        print("❌ Nenhum run encontrado.")
        return

    latest_run = runs[-1]
    print(f"📂 Analisando Run: {latest_run.name}")
    
    pages_data = []
    total_score = 0
    
    for page_dir in latest_run.iterdir():
        if not page_dir.is_dir(): continue
        
        summary_path = page_dir / "docs" / "inda_summary.json"
        if summary_path.exists():
            with open(summary_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                pages_data.append(data)
                total_score += data.get("score", {}).get("total", 0)

    if not pages_data:
        print("⚠️ Nenhum sumário INDA encontrado.")
        return

    avg_score = int(total_score / len(pages_data))
    
    if avg_score >= 90:
        verdict = "✅ PRONTO PARA PRODUÇÃO"
    elif avg_score >= 70:
        verdict = "⚠️ APROVADO COM RESSALVAS"
    else:
        verdict = "❌ BLOQUEADO"

    report_path = OUTPUT_ROOT / "README_EXECUTIVO.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 📊 Relatório Executivo de Qualidade (v5.1)\n")
        f.write(f"**Run ID:** {latest_run.name}\n")
        f.write(f"**Data:** {latest_run.name.replace('run_', '')}\n\n")
        
        f.write(f"## Veredito: {verdict}\n")
        f.write(f"- **Score Global:** {avg_score}/100\n")
        f.write(f"- **Páginas Auditadas:** {len(pages_data)}\n\n")
        
        f.write("### 🚦 Detalhamento por Página\n")
        f.write("| Página | Score | Risco | Status HTTP | Elementos | Sucesso |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for p in sorted(pages_data, key=lambda x: x['score']['total']):
            risk_icon = "🔴" if p['risk'] == "HIGH" else "🟢"
            f.write(f"| {p['page']} | {p['score']['total']} | {risk_icon} {p['risk']} | {p['status_http']} | {p['elements_total']} | {p['interactions_success']} |\n")

    print(f"📄 Relatório Executivo gerado em: {report_path}")

if __name__ == "__main__":
    generate_executive_report()

