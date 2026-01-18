# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 11:15:00
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# ==============================================================================
# 🔄 MASS REGISTRY SYNCHRONIZER v5.2 (Gold Master Edition)
# ==============================================================================
# Objetivo: Sincronizar o inventário físico de scripts com o Registry XML.
# SSOT: governance/registry.xml
# ==============================================================================

REGISTRY_PATH = Path("governance/registry.xml")
SEARCH_DIRS = [
    Path("scripts"),
    Path("canonic")
]
IGNORE_DIRS = {
    "__pycache__", "node_modules", ".pytest_cache", "tests", "_archive", "ignorar"
}
IGNORE_FILES = {
    "__init__.py", "conftest.py"
}

def get_physical_scripts():
    """Varre os diretórios canônicos em busca de scripts Python."""
    physical = set()
    for d in SEARCH_DIRS:
        if not d.exists():
            continue
        for root, dirs, files in os.walk(d):
            # Poda diretórios ignorados
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                if file.endswith(".py") and file not in IGNORE_FILES:
                    physical.add(file)
    return physical

def sync():
    print("🔄 Iniciando Sincronização de Registro (Padrão L10)...")
    
    # Garante que a pasta de governança existe
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1. Carregamento ou Inicialização do XML
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
                xml_content = f.read().strip()
            root = ET.fromstring(xml_content)
            tree = ET.ElementTree(root)
        except Exception as e:
            print(f"⚠️ Erro ao ler XML existente: {e}. Criando novo.")
            root = ET.Element("Registry", version="5.1")
            tree = ET.ElementTree(root)
    else:
        root = ET.Element("Registry", version="5.1")
        tree = ET.ElementTree(root)

    # 2. Garantir estrutura básica
    meta = root.find("Meta")
    if meta is None:
        meta = ET.SubElement(root, "Meta")
        ET.SubElement(meta, "Status").text = "GOLD_MASTER_CANDIDATE"
        ET.SubElement(meta, "Authority").text = "Optimus Kernel L6"

    scripts_node = root.find("Scripts")
    if scripts_node is None:
        scripts_node = ET.SubElement(root, "Scripts")

    # 3. Cruzamento de Dados
    registered_names = {s.get("name") for s in scripts_node.findall("Script")}
    physical_scripts = get_physical_scripts()
    
    added_count = 0
    for script_name in physical_scripts:
        if script_name not in registered_names:
            new_script = ET.SubElement(scripts_node, "Script")
            # Gera um ID amigável baseado no nome
            script_id = script_name.upper().replace(".PY", "").replace("_", "-")[:15]
            
            new_script.set("id", script_id)
            new_script.set("name", script_name)
            new_script.set("status", "PENDING")
            new_script.set("blocking", "false")
            
            print(f"   [+] Novo script detectado: {script_name}")
            added_count += 1

    # 4. Salvamento Atômico (Garante conformidade XML na linha 1)
    if added_count > 0:
        ET.indent(tree, space="    ", level=0)
        with open(REGISTRY_PATH, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding="UTF-8", xml_declaration=False)
        print(f"\n✅ Sincronização concluída. {added_count} scripts adicionados ao Registry.")
    else:
        print("\n✨ O Registry já está sincronizado com os arquivos físicos.")

if __name__ == "__main__":
    sync()

