import os
import sys
import io
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🏁 CANONIC PROTOCOL FINALIZER
# ==============================================================================
# Objetivo: Varrer a pasta canonic/ (os sobreviventes do filtro), gerar o 
# registry.xml oficial e criar um README de inventário.
# ==============================================================================

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TARGET_DIR = Path("canonic")
REGISTRY_FILE = TARGET_DIR / "registry.xml"
README_FILE = TARGET_DIR / "README.md"

def finalize_protocol():
    print(f"🚀 Finalizando Protocolo Canônico em: {TARGET_DIR.absolute()}")
    
    if not TARGET_DIR.exists():
        print("❌ Pasta canonic/ não encontrada. Rode o filtro primeiro.")
        return

    # 1. Coletar Scripts Sobreviventes
    survivors = sorted([f for f in TARGET_DIR.glob("*.py") if "finalize" not in f.name])
    
    if not survivors:
        print("⚠️ Nenhum script encontrado em canonic/.")
        return

    # 2. Gerar Registry XML
    root = ET.Element("Registry", version="5.0", authority="MesaFlow Great Filter")
    meta = ET.SubElement(root, "Meta")
    ET.SubElement(meta, "Status").text = "SEALED"
    ET.SubElement(meta, "CertifiedAt").text = datetime.now().isoformat()
    ET.SubElement(meta, "SurvivorCount").text = str(len(survivors))
    
    scripts_node = ET.SubElement(root, "Scripts")
    
    print(f"📝 Protocolando {len(survivors)} scripts...")
    
    markdown_lines = [
        "# 🛡️ MesaFlow Canonic Scripts (Elite)",
        f"**Data de Certificação:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "**Status:** ✅ TESTED & APPROVED",
        "",
        "Estes scripts sobreviveram ao 'Great Filter' e constituem a ferramenta operacional confiável do sistema.",
        "",
        "| ID | Script | Status |",
        "| :--- | :--- | :---: |"
    ]

    for script in survivors:
        # Gerar ID determinístico
        script_id = f"CANON-{abs(hash(script.name)) % 10000:04d}"
        
        # XML Entry
        entry = ET.SubElement(scripts_node, "Script")
        entry.set("id", script_id)
        entry.set("name", script.name)
        entry.set("status", "SUCCESS")
        entry.set("blocking", "false")
        
        # Markdown Entry
        markdown_lines.append(f"| `{script_id}` | `{script.name}` | 🟢 OPERATIONAL |")

    # 3. Salvar XML
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ", level=0)
    tree.write(REGISTRY_FILE, encoding="utf-8", xml_declaration=True)
    print(f"✅ Registry salvo: {REGISTRY_FILE}")

    # 4. Salvar README
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_lines))
    print(f"✅ README salvo: {README_FILE}")

    print("\n🎉 PROCESSO CONCLUÍDO.")
    print("A pasta 'canonic/' agora contém apenas a elite dos scripts funcionais.")

if __name__ == "__main__":
    finalize_protocol()

