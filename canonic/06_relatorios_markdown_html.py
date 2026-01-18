# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 10:35:00
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Relatorios")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>MesaFlow UI Audit Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .heatmap-5 { background-color: #16a34a; } /* 100% */
        .heatmap-4 { background-color: #22c55e; } /* 80% */
        .heatmap-3 { background-color: #eab308; } /* 60% */
        .heatmap-2 { background-color: #f97316; } /* 40% */
        .heatmap-1 { background-color: #ef4444; } /* 20% */
        .heatmap-0 { background-color: #475569; } /* 0% */
    </style>
</head>
<body class="bg-slate-950 text-slate-200 font-sans p-8">
    <div class="max-w-7xl mx-auto">
        <header class="flex justify-between items-end mb-12 border-b border-slate-800 pb-8">
            <div>
                <h1 class="text-4xl font-black text-white tracking-tighter">UI AUDIT <span class="text-orange-500">DASHBOARD</span></h1>
                <p class="text-slate-500 mt-2 font-mono uppercase text-xs tracking-widest">MesaFlow OS v5.1 • {{TIMESTAMP}}</p>
            </div>
            <div class="text-right">
                <div class="text-5xl font-black text-orange-500">{{COVERAGE}}%</div>
                <div class="text-xs font-bold text-slate-500 uppercase tracking-widest">Cobertura Ponderada</div>
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
            <div class="bg-slate-900 p-6 rounded-3xl border border-slate-800">
                <p class="text-slate-500 text-xs font-bold uppercase mb-1">Total de Telas</p>
                <p class="text-3xl font-black text-white">{{TOTAL}}</p>
            </div>
            <div class="bg-slate-900 p-6 rounded-3xl border border-slate-800">
                <p class="text-slate-500 text-xs font-bold uppercase mb-1">Críticos OK</p>
                <p class="text-3xl font-black text-green-500">{{CRITICAL_OK}}/{{CRITICAL_TOTAL}}</p>
            </div>
            <div class="bg-slate-900 p-6 rounded-3xl border border-slate-800">
                <p class="text-slate-500 text-xs font-bold uppercase mb-1">Score Médio</p>
                <p class="text-3xl font-black text-blue-500">{{AVG_SCORE}}%</p>
            </div>
            <div class="bg-slate-900 p-6 rounded-3xl border border-slate-800">
                <p class="text-slate-500 text-xs font-bold uppercase mb-1">Status CI</p>
                <p class="text-xl font-black {{GATE_COLOR}}">{{GATE}}</p>
            </div>
        </div>

        <div class="bg-slate-900 rounded-3xl border border-slate-800 overflow-hidden">
            <table class="w-full text-left text-sm">
                <thead class="bg-slate-800 text-slate-400 uppercase text-[10px] font-black tracking-widest">
                    <tr>
                        <th class="p-4">Prioridade</th>
                        <th class="p-4">Tela</th>
                        <th class="p-4">Plataforma</th>
                        <th class="p-4">Score</th>
                        <th class="p-4">Heatmap de Seções</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800">
                    {{TABLE_ROWS}}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    metrics_path = Path("docs/audit/ui_audit_metrics.json")
    if not results_path.exists() or not metrics_path.exists(): return

    with open(results_path, "r") as f: results = json.load(f)
    with open(metrics_path, "r") as f: metrics = json.load(f)
    
    # 1. Gerar Markdown
    md = ["# 📊 Relatório de Cobertura de UI", f"> Gerado em: {datetime.now().isoformat()}", ""]
    md.append(f"| Prioridade | Tela | Plataforma | Score | Status |")
    md.append(f"| :--- | :--- | :--- | :--- | :--- |")
    
    rows = ""
    for s in sorted(results, key=lambda x: (not x.get('is_critical'), -x.get('score', 0))):
        prio = "🔴 ALTA" if s.get("is_critical") else "🟡 MÉDIA"
        status = s.get("status", "UNKNOWN")
        md.append(f"| {prio} | {s['normalized_name']} | {s['platform']} | {s['score']}% | {status} |")
        
        # HTML Row
        prio_class = "text-red-500" if s.get("is_critical") else "text-yellow-500"
        sections_count = s.get("sections_count", 0)
        rows += f"""
        <tr class="hover:bg-slate-800/50 transition-colors">
            <td class="p-4 font-bold {prio_class}">{prio}</td>
            <td class="p-4 font-bold text-white">{s['normalized_name']}</td>
            <td class="p-4 uppercase text-xs font-mono text-slate-500">{s['platform']}</td>
            <td class="p-4 font-black">{s['score']}%</td>
            <td class="p-4">
                <div class="flex gap-1">
                    {''.join([f'<div class="w-4 h-4 rounded-sm heatmap-{sections_count}"></div>' for _ in range(5)])}
                </div>
            </td>
        </tr>
        """

    Path("docs/audit/UI_COVERAGE_REPORT.md").write_text("\n".join(md), encoding="utf-8")
    
    # 2. Gerar HTML
    html = HTML_TEMPLATE.replace("{{TIMESTAMP}}", datetime.now().strftime("%d/%m/%Y %H:%M"))
    html = html.replace("{{COVERAGE}}", str(metrics['weighted_coverage']))
    html = html.replace("{{TOTAL}}", str(metrics['total_screens']))
    html = html.replace("{{CRITICAL_OK}}", str(metrics['critical_ok']))
    html = html.replace("{{CRITICAL_TOTAL}}", str(metrics['critical_total']))
    html = html.replace("{{AVG_SCORE}}", str(metrics['avg_score']))
    html = html.replace("{{GATE}}", metrics['ci_gate'])
    html = html.replace("{{GATE_COLOR}}", "text-green-500" if metrics['ci_gate'] == "PASS" else "text-red-500")
    html = html.replace("{{TABLE_ROWS}}", rows)
    
    Path("docs/audit/UI_EXECUTIVE_DASHBOARD.html").write_text(html, encoding="utf-8")
    logger.info("Relatórios Markdown e HTML gerados com sucesso.")

if __name__ == "__main__":
    run()

