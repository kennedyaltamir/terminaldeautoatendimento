# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 04:15:00
import json
import os
from datetime import datetime
from pathlib import Path

# Configuração de Caminhos
INPUT_FILE = Path("docs/audit/UI_INVENTORY_FULL.json")
OUTPUT_DIR = Path("docs/sds/UI_DOCS")
OUTPUT_FILE = OUTPUT_DIR / "FULL_UI_REFERENCE.md"

def load_inventory():
    if not INPUT_FILE.exists():
        print(f"❌ Erro: Arquivo de inventário não encontrado: {INPUT_FILE}")
        print("👉 Execute 'node scripts/automation/generate_ui_inventory.js' primeiro.")
        return None
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return None

def format_elements_table(elements):
    if not elements:
        return "_Nenhum elemento interativo detectado._"
    
    md = "| Tipo | Nome/Label | Ação Esperada | Validação/Estado |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    
    for el in elements:
        tipo = el.get('tipo', 'unknown')
        nome = el.get('nome', '-')
        acao = el.get('acao', '-')
        validacao = el.get('validacao', '-')
        
        # Formatação visual
        if tipo == 'botao' or tipo == 'button':
            tipo = f"**{tipo.upper()}**"
        
        md += f"| {tipo} | {nome} | {acao} | {validacao} |\n"
    
    return md

def format_layout(layout):
    if not layout:
        return "_Layout não estruturado._"
    return "\n".join([f"- `{item}`" for item in layout])

def generate_screen_doc(screen, platform):
    md = f"## 📱 Tela: {screen.get('tela', 'Sem Título')}\n"
    md += f"**Plataforma:** {platform} | **Rota:** `{screen.get('rota', 'N/A')}`\n\n"
    
    md += "### 1. Layout e Estrutura\n"
    md += format_layout(screen.get('layout', [])) + "\n\n"
    
    md += "### 2. Elementos Interativos\n"
    md += format_elements_table(screen.get('elementos', [])) + "\n\n"
    
    md += "### 3. Fluxo e Estados\n"
    flows = screen.get('fluxo', [])
    states = screen.get('estados_detectados', []) or screen.get('estados_codigo', [])
    
    if flows:
        md += "**Navegação:**\n" + "\n".join([f"- ➡️ {f}" for f in flows]) + "\n"
    
    if states:
        md += "\n**Estados Detectados:** " + ", ".join([f"`{s}`" for s in states]) + "\n"
    
    md += "\n### 4. Observações Automáticas\n"
    if 'error' in states or 'erro' in screen:
        md += "⚠️ **Atenção:** Esta tela apresentou erros durante a varredura.\n"
    elif not screen.get('elementos'):
        md += "ℹ️ **Nota:** Tela informativa, sem interações detectadas.\n"
    else:
        md += "✅ Estrutura interativa validada.\n"
    
    md += "\n---\n\n"
    return md

def main():
    print("📚 Gerando Documentação de UI (Markdown)...")
    data = load_inventory()
    if not data: return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    content = [
        "# 🎨 MesaFlow OS - Referência de Interface (UI Docs)",
        f"> **Gerado em:** {datetime.now().isoformat()}",
        f"> **Versão do Inventário:** {data.get('meta', {}).get('version', 'N/A')}",
        "",
        "Este documento detalha a estrutura, interatividade e fluxos de todas as telas do sistema.",
        "",
        "## Índice",
        "- [Web / Admin](#web--admin)",
        "- [Mobile (App)](#mobile-app)",
        "",
        "---",
        "",
        "## Web / Admin",
        ""
    ]

    # Processar Web
    for screen in data.get('web', []):
        content.append(generate_screen_doc(screen, "WEB"))

    content.append("## Mobile (App)")
    content.append("")

    # Processar Mobile
    for screen in data.get('mobile', []):
        content.append(generate_screen_doc(screen, "MOBILE"))

    # Salvar
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    
    print(f"✅ Documentação gerada em: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

