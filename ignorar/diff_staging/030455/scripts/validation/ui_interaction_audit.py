import os
import re
import sys
import io
from pathlib import Path

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
    links = re.findall(r'<Link(.*?)>', content, re.DOTALL)
    inputs = re.findall(r'<input(.*?)>', content, re.DOTALL)
    
    issues = []
    button_count = 0
    
    # Análise de Botões (Improved Logic)
    for match in re.finditer(r'<button(.*?)>', content, re.DOTALL):
        button_count += 1
        attrs = match.group(1)
        
        has_click = "onClick" in attrs
        has_submit = 'type="submit"' in attrs or "type='submit'" in attrs
        has_form_action = "formAction" in attrs
        is_radix = "asChild" in attrs
        
        if not (has_click or has_submit or has_form_action or is_radix):
            # Heurística para detectar truncamento por '>' em atributos (ex: disabled={a > b})
            # Se houver '{' mas não '}', pode indicar que o regex parou cedo demais.
            # Mas o regex (.*?) é non-greedy e para no primeiro >.
            # Se houver um > dentro de uma expressão JS, o regex falha.
            # A correção real é no código (extrair lógica), mas aqui podemos tentar ser menos alarmistas.
            
            # Verifica se parece ser um botão de UI library que usa props espalhadas {...props}
            if "{...props}" in attrs or "{...rest}" in attrs:
                continue
                
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
        "buttons": button_count,
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
