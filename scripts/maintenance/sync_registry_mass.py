
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 10:55:00
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# ==============================================================================
# 🔄 MASS REGISTRY SYNCHRONIZER (ROBUST)
# ==============================================================================
# Objetivo: Adicionar todos os scripts físicos órfãos ao registry.xml.
# Fix: Leitura tolerante a whitespace no XML.
# ==============================================================================

REGISTRY_PATH = Path("comunication/registry.xml")
SEARCH_DIRS = [
    Path("scripts"),
    Path("comunication/scripts")
]
IGNORE_DIRS = {
    "__pycache__", "node_modules", ".pytest_cache", "tests"
}
IGNORE_FILES = {
    "__init__.py", "conftest.py"
}

def get_physical_scripts():
    physical = set()
    for d in SEARCH_DIRS:
        for root, dirs, files in os.walk(d):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                if file.endswith(".py") and file not in IGNORE_FILES:
                    physical.add(file)
    return physical

def sync():
    print("🔄 Running Mass Registry Sync (Robust)...")
    
    if not REGISTRY_PATH.exists():
        print("❌ Registry not found.")
        return

    try:
        # L5 Self-Correction: Lê como string e remove whitespace
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            xml_content = f.read().strip()
        
        root = ET.fromstring(xml_content)
        tree = ET.ElementTree(root)
    except Exception as e:
        print(f"❌ Error parsing registry: {e}")
        return

    scripts_node = root.find("Scripts")
    if scripts_node is None:
        scripts_node = ET.SubElement(root, "Scripts")

    registered_names = {s.get("name") for s in scripts_node.findall("Script")}
    physical_scripts = get_physical_scripts()
    
    added_count = 0
    
    for script_name in physical_scripts:
        if script_name not in registered_names:
            new_script = ET.SubElement(scripts_node, "Script")
            script_id = script_name.upper().replace(".PY", "").replace("_", "-")[:15]
            
            new_script.set("id", script_id)
            new_script.set("name", script_name)
            new_script.set("status", "PENDING")
            new_script.set("blocking", "false")
            
            print(f"   ➕ Added: {script_name}")
            added_count += 1

    if added_count > 0:
        ET.indent(tree, space="    ", level=0)
        # Salva garantindo sem linha em branco no inicio
        with open(REGISTRY_PATH, "wb") as f:
            tree.write(f, encoding="UTF-8", xml_declaration=True)
        print(f"\n✅ Sync Complete. {added_count} scripts added to Registry.")
    else:
        print("\n✨ Registry is already up to date.")

if __name__ == "__main__":
    sync()

