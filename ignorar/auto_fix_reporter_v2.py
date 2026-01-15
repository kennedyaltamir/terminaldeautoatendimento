
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 12:05:00
import os
from pathlib import Path

# ==============================================================================
# 🛠️ AUTO FIX REPORTER v2 (Executive Edition)
# ==============================================================================
# Gera o README_EXECUTIVO.md com análise de risco e prontidão.
# ==============================================================================

REPORT_DIR = Path("testesvisuais/fotos")
OUTPUT_ROOT = Path("testesvisuais")

def generate_executive_report():
    print("🔍 Gerando Relatório Executivo de Prontidão...")
    
    runs = sorted([d for d in REPORT_DIR.iterdir() if d.is_dir() and d.name.startswith("run_")])
    if not runs:
        print("❌ Nenhum dado encontrado.")
        return

    latest_run = runs[-1]
    inventory_file = latest_run / "todososbotoeseclicaveis.md"
    
    if not inventory_file.exists():
        return

    # Análise dos dados
    total_pages = 0
    total_score = 0
    critical_pages = []
    
    with open(inventory_file, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line and "Página" not in line and "---" not in line:
                parts = line.split("|")
                if len(parts) > 4:
                    page = parts[1].strip()
                    score_str = parts[4].strip().split("/")[0]
                    try:
                        score = int(score_str)
                        total_pages += 1
                        total_score += score
                        if score < 70:
                            critical_pages.append(page)
                    except:
                        pass

    avg_score = int(total_score / total_pages) if total_pages > 0 else 0
    
    # Determinação de Status
    if avg_score >= 90 and not critical_pages:
        status = "✅ PRONTO PARA PRODUÇÃO"
        color = "green"
    elif avg_score >= 70:
        status = "⚠️ APROVADO COM RESSALVAS"
        color = "yellow"
    else:
        status = "❌ NÃO RECOMENDADO"
        color = "red"

    # Escrita do Relatório Executivo
    exec_report = OUTPUT_ROOT / "README_EXECUTIVO.md"
    with open(exec_report, "w", encoding="utf-8") as f:
        f.write(f"# 📊 Relatório Executivo de Qualidade\n")
        f.write(f"**Data:** {latest_run.name.replace('run_', '')}\n\n")
        
        f.write(f"## Veredito Final: {status}\n")
        f.write(f"- **Score Global de UX/QA:** {avg_score}/100\n")
        f.write(f"- **Páginas Auditadas:** {total_pages}\n")
        f.write(f"- **Páginas Críticas:** {len(critical_pages)}\n\n")
        
        if critical_pages:
            f.write("### 🚨 Pontos de Atenção Imediata\n")
            for p in critical_pages:
                f.write(f"- {p}\n")
        
        f.write("\n### 📝 Recomendações\n")
        if avg_score < 90:
            f.write("1. Corrigir erros de carregamento nas páginas críticas.\n")
            f.write("2. Validar fluxos de interação que falharam no teste comportamental.\n")
        else:
            f.write("1. O sistema apresenta estabilidade visual e funcional.\n")
            f.write("2. Liberado para deploy em Staging/Produção.\n")

    print(f"📄 Relatório Executivo gerado em: {exec_report}")

if __name__ == "__main__":
    generate_executive_report()

