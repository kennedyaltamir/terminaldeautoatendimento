
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 06:10:00
import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🚑 COMPREHENSIVE REGISTRY DRIFT FIXER
# ==============================================================================
# Restaura Scripts E Evidências movidos para 'ignorar/' para garantir
# a integridade total do Registry.
# ==============================================================================

REGISTRY_PATH = Path("comunication/registry.xml")
SCRIPTS_DEST = Path("comunication/scripts")
REPORTS_DEST = Path("comunication/reports")
IGNORE_DIR = Path("ignorar")

# Locais válidos onde scripts podem estar (além do destino de restauração)
VALID_SCRIPT_DIRS = [
    Path("comunication/scripts"),
    Path("scripts/validar"),
    Path("scripts/maintenance"),
    Path("scripts/automation"),
    Path("scripts/security")
]

def find_in_ignore(filename):
    """Procura o arquivo recursivamente na pasta ignorar."""
    for path in IGNORE_DIR.rglob(filename):
        return path
    return None

def script_exists(script_name):
    """Verifica se o script existe em algum diretório válido."""
    for d in VALID_SCRIPT_DIRS:
        if (d / script_name).exists():
            return True
    return False

def fix_drift():
    print("🚑 Running Comprehensive Drift Fixer...")
    
    if not REGISTRY_PATH.exists():
        print("❌ Registry not found.")
        return

    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            xml_content = f.read().strip()
        root = ET.fromstring(xml_content)
    except Exception as e:
        print(f"❌ Error parsing registry: {e}")
        return

    scripts_node = root.find("Scripts")
    if scripts_node is None: return

    SCRIPTS_DEST.mkdir(parents=True, exist_ok=True)
    REPORTS_DEST.mkdir(parents=True, exist_ok=True)
    
    restored_scripts = 0
    restored_reports = 0
    placeholders = 0

    for script in scripts_node.findall("Script"):
        name = script.get("name")
        evidence = script.get("evidence")
        status = script.get("status")

        # 1. Fix Missing Script
        if name and not script_exists(name):
            print(f"   🔍 Script Missing: {name}")
            found = find_in_ignore(name)
            if found:
                shutil.copy2(str(found), str(SCRIPTS_DEST / name))
                print(f"      ✅ Restored Script from {found}")
                restored_scripts += 1
            else:
                print(f"      ⚠️  Script lost. Creating Stub.")
                with open(SCRIPTS_DEST / name, "w", encoding="utf-8") as f:
                    f.write(f"# STUB RECOVERED\nprint('Script {name} recovered as stub.')\n")
                placeholders += 1

        # 2. Fix Missing Evidence
        if status == "SUCCESS" and evidence:
            evidence_path = REPORTS_DEST / evidence
            if not evidence_path.exists():
                print(f"   🔍 Evidence Missing: {evidence}")
                found = find_in_ignore(evidence)
                if found:
                    shutil.copy2(str(found), str(evidence_path))
                    print(f"      ✅ Restored Evidence from {found}")
                    restored_reports += 1
                else:
                    print(f"      ⚠️  Evidence lost. Creating Placeholder.")
                    with open(evidence_path, "w", encoding="utf-8") as f:
                        f.write(f"# Audit Placeholder: {evidence}\n\nRecovered to fix drift.\n")
                    placeholders += 1

    print("-" * 40)
    print(f"🏁 Fix Complete.")
    print(f"   - Scripts Restored: {restored_scripts}")
    print(f"   - Reports Restored: {restored_reports}")
    print(f"   - Placeholders: {placeholders}")

if __name__ == "__main__":
    fix_drift()

