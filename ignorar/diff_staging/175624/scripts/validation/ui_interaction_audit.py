# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 17:05:00
import os
import re
from pathlib import Path

# ==============================================================================
# 🖱️ UI INTERACTION AUDITOR (Static Analysis)
# ==============================================================================
# Varre o código Frontend em busca de elementos interativos (Botões, Links, Inputs)
# e verifica se eles possuem handlers (onClick, href, onChange) ou se são "mortos".
# ==============================================================================

FRONTEND_ROOT = Path("frontend/src")
REPORT_PATH = Path("governance/evidence/REPORT_UI_INTERACTIONS.md")

def analyze_file(path):
    content = path.read_text(encoding="utf-8")
    
    # Regex para encontrar elementos
    buttons = re.findall(r'<button(.*?)>', content, re.DOTALL)
    links = re.findall(r'<Link(.*?)>', content, re.DOTALL)
    inputs = re.findall(r'<input(.*?)>', content, re.DOTALL)
    
    issues = []
    
    # Análise de Botões
    for i, btn in enumerate(buttons):
        if "onClick" not in btn and "type=\"submit\"" not in btn and "formAction" not in btn:
            # Ignora botões que são apenas triggers de menu (ex: Radix UI) se tiverem atributos específicos
            if "asChild" not in btn:
                issues.append(f"⚠️ Botão sem ação (onClick/submit) na linha aprox.")

    # Análise de Links
    for i, link in enumerate(links):
        if "href" not in link:
            issues.append(f"❌ Link sem destino (href) na linha aprox.")

    # Análise de Inputs
    for i, inp in enumerate(inputs):
        if "onChange" not in inp and "register" not in inp and "readOnly" not in inp and "type=\"hidden\"" not in inp:
             # Inputs controlados sem onChange são read-only de fato, mas podem ser erro
             issues.append(f"⚠️ Input potencialmente não controlado (sem onChange/register).")

    return {
        "buttons": len(buttons),
        "links": len(links),
        "inputs": len(inputs),
        "issues": issues
    }

def run_audit():
    print("🖱️  Iniciando Auditoria de Interatividade de UI...")
    
    results = {}
    total_elements = 0
    total_issues = 0
    
    for path in FRONTEND_ROOT.rglob("*.tsx"):
        if "components/ui" in str(path): continue # Pula componentes base (shadcn)
        
        analysis = analyze_file(path)
        if analysis["buttons"] + analysis["links"] + analysis["inputs"] > 0:
            rel_path = str(path.relative_to(FRONTEND_ROOT))
            results[rel_path] = analysis
            total_elements += (analysis["buttons"] + analysis["links"] + analysis["inputs"])
            total_issues += len(analysis["issues"])

    # Gerar Relatório
    os.makedirs(REPORT_PATH.parent, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"# 🖱️ Relatório de Interatividade de UI\n")
        f.write(f"**Total de Elementos Interativos:** {total_elements}\n")
        f.write(f"**Potenciais Problemas:** {total_issues}\n\n")
        
        f.write("| Arquivo | Botões | Links | Inputs | Alertas |\n")
        f.write("| :--- | :---: | :---: | :---: | :--- |\n")
        
        for file, data in sorted(results.items()):
            status = "✅" if not data["issues"] else "⚠️"
            issues_str = "<br>".join(data["issues"][:3]) # Limita a 3 erros por linha
            if len(data["issues"]) > 3: issues_str += "<br>..."
            
            f.write(f"| `{file}` | {data['buttons']} | {data['links']} | {data['inputs']} | {status} {issues_str} |\n")

    print(f"✅ Auditoria concluída. {total_elements} elementos analisados.")
    print(f"📄 Relatório gerado: {REPORT_PATH}")

if __name__ == "__main__":
    run_audit()
