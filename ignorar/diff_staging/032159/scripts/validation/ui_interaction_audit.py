import os
import re
import sys
import io
from pathlib import Path

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 🖱️ UI INTERACTION AUDITOR v2.0 (JSX-Aware)
# ==============================================================================
# Varre o código Frontend em busca de elementos interativos.
# Implementa um parser de estado simples para lidar com JSX e Arrow Functions
# que contêm caracteres '>' dentro de props.
# ==============================================================================

FRONTEND_ROOT = Path("frontend/src")
REPORT_PATH = Path("governance/evidence/REPORT_UI_INTERACTIONS.md")

def extract_tags(content, tag_name):
    """
    Extrai tags completas lidando com aninhamento de chaves {} do JSX.
    Retorna uma lista de strings contendo os atributos da tag.
    """
    tags = []
    # Encontra o início de todas as tags
    start_indices = [m.start() for m in re.finditer(f"<{tag_name}\\b", content)]
    
    for start in start_indices:
        balance = 0
        in_quote = False
        quote_char = ''
        i = start
        
        # Avança até encontrar o fechamento da tag >
        while i < len(content):
            char = content[i]
            
            if in_quote:
                if char == quote_char:
                    in_quote = False
            else:
                if char == '"' or char == "'":
                    in_quote = True
                    quote_char = char
                elif char == '{':
                    balance += 1
                elif char == '}':
                    balance -= 1
                elif char == '>' and balance == 0:
                    # Fim da tag encontrado
                    tags.append(content[start:i])
                    break
            i += 1
            
    return tags

def analyze_file(path):
    content = path.read_text(encoding="utf-8")
    
    # Extração robusta
    buttons = extract_tags(content, "button")
    links = extract_tags(content, "Link")
    inputs = extract_tags(content, "input")
    
    issues = []
    
    # Análise de Botões
    for btn in buttons:
        has_click = "onClick" in btn
        has_submit = 'type="submit"' in btn or "type='submit'" in btn
        has_form_action = "formAction" in btn
        is_radix = "asChild" in btn
        has_spread = "{...props}" in btn or "{...rest}" in btn
        
        if not (has_click or has_submit or has_form_action or is_radix or has_spread):
            # Tenta pegar o número da linha (aproximado)
            line_num = content[:content.find(btn)].count('\n') + 1
            issues.append(f"⚠️ Botão sem ação (onClick/submit) na linha {line_num}")

    # Análise de Links
    for link in links:
        if "href" not in link:
            line_num = content[:content.find(link)].count('\n') + 1
            issues.append(f"❌ Link sem destino (href) na linha {line_num}")

    # Análise de Inputs
    for inp in inputs:
        if "onChange" not in inp and "register" not in inp and "readOnly" not in inp and "type=\"hidden\"" not in inp:
             line_num = content[:content.find(inp)].count('\n') + 1
             issues.append(f"⚠️ Input potencialmente não controlado na linha {line_num}")

    return {
        "buttons": len(buttons),
        "links": len(links),
        "inputs": len(inputs),
        "issues": issues
    }

def run_audit():
    print("🖱️  Iniciando Auditoria de Interatividade de UI (JSX-Aware)...")
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
