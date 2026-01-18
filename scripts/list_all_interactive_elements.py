import os
import re
from pathlib import Path

# ==============================================================================
# 🕵️ INTERACTIVE ELEMENT LISTER (Deep Scan)
# ==============================================================================
# Objetivo: Listar EXPLICITAMENTE todos os elementos interativos encontrados
# no código fonte do Frontend para auditoria manual pré-deploy.
# ==============================================================================

FRONTEND_ROOT = Path("frontend/src")
OUTPUT_FILE = Path("docs/audit/INTERACTIVE_ELEMENTS_LIST.md")

# Padrões de Elementos Interativos
PATTERNS = {
    "Button": r"<button.*?>.*?</button>|<button.*?>",
    "Link": r"<Link.*?>.*?</Link>|<Link.*?>",
    "Anchor": r"<a\s.*?>.*?</a>|<a\s.*?>",
    "Input": r"<input.*?>",
    "Textarea": r"<textarea.*?>.*?</textarea>|<textarea.*?>",
    "Select": r"<select.*?>.*?</select>|<select.*?>",
    "Clickable Div/Span": r"<(div|span)[^>]*onClick=.*?>",
    "Form": r"<form.*?>",
}

def scan_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
    except:
        return None

    elements = []
    lines = content.splitlines()

    for i, line in enumerate(lines):
        line_num = i + 1
        clean_line = line.strip()
        
        for type_name, regex in PATTERNS.items():
            if re.search(regex, clean_line):
                # Tenta capturar o contexto (atributos importantes)
                # Simplificação: Pega a linha inteira truncada
                snippet = clean_line[:150].replace("`", "'")
                if len(clean_line) > 150: snippet += "..."
                
                elements.append({
                    "line": line_num,
                    "type": type_name,
                    "snippet": snippet
                })
                # Para no primeiro match por linha para evitar duplicatas óbvias
                break
    
    return elements

def generate_report():
    print("🕵️  Iniciando Varredura Profunda de Elementos Interativos...")
    
    report_lines = [
        "# 🖱️ Inventário Completo de Elementos Interativos",
        f"**Data:** {os.times()}",
        "",
        "Este documento lista todos os pontos de interação detectados estaticamente no código.",
        "Use-o para validar se todos os botões, links e inputs estão mapeados e funcionais.",
        ""
    ]

    total_files = 0
    total_elements = 0

    # Varre apenas arquivos relevantes (Páginas e Componentes)
    for root, _, files in os.walk(FRONTEND_ROOT):
        for file in files:
            if not file.endswith(".tsx"): continue
            
            file_path = Path(root) / file
            rel_path = file_path.relative_to(FRONTEND_ROOT)
            
            # Ignora arquivos de teste e stories
            if "test" in file or "stories" in file: continue

            elements = scan_file(file_path)
            
            if elements:
                total_files += 1
                total_elements += len(elements)
                report_lines.append(f"## 📄 `{rel_path}`")
                report_lines.append("| Linha | Tipo | Snippet (Código) |")
                report_lines.append("| :---: | :--- | :--- |")
                
                for el in elements:
                    # Escapa pipes para não quebrar a tabela MD
                    safe_snippet = el['snippet'].replace("|", "\|").replace("<", "&lt;").replace(">", "&gt;")
                    report_lines.append(f"| {el['line']} | **{el['type']}** | `{safe_snippet}` |")
                
                report_lines.append("")

    # Resumo
    summary = [
        "## Resumo Executivo",
        f"- **Arquivos com Interação:** {total_files}",
        f"- **Total de Elementos:** {total_elements}",
        "---",
        ""
    ]
    
    final_content = "\n".join(summary + report_lines)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(final_content, encoding="utf-8")
    
    print(f"✅ Inventário gerado com sucesso: {total_elements} elementos encontrados.")
    print(f"📄 Relatório salvo em: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_report()

