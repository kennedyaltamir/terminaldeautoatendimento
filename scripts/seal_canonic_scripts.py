# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-16 11:06:00
import xml.etree.ElementTree as ET
from pathlib import Path

REGISTRY_PATH = Path("governance/registry.xml")

def seal():
    print("🛡️  Selando Scripts Canônicos no Registro...")
    
    if not REGISTRY_PATH.exists():
        print("❌ Erro: Registry não encontrado.")
        return

    tree = ET.parse(REGISTRY_PATH)
    root = tree.getroot()
    
    scripts_node = root.find("Scripts")
    updated_count = 0
    
    # Lista de scripts que acabamos de validar com 100%
    canonic_scripts = [
        "01_varredura.py", "02_auditoria_markdown.py", 
        "03_normal_roteamento.py", "05_calculo_metricas.py", 
        "06_relatorios_markdown_html.py"
    ]
    
    for script in scripts_node.findall("Script"):
        if script.get("name") in canonic_scripts:
            script.set("status", "SUCCESS")
            updated_count += 1
            print(f"   [✅] Selado: {script.get('name')}")

    if updated_count > 0:
        ET.indent(tree, space="    ", level=0)
        with open(REGISTRY_PATH, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding="UTF-8", xml_declaration=False)
        print(f"\n✨ Sucesso! {updated_count} scripts marcados como SUCCESS.")
    else:
        print("⚠️  Nenhum script canônico encontrado para selagem.")

if __name__ == "__main__":
    seal()

