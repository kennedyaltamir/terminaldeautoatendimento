# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:35:00
import os
import sys
import io
import xml.etree.ElementTree as ET
from pathlib import Path

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# SSOT: O Registry agora reside em /governance
REGISTRY_PATH = Path("governance/registry.xml")
SCRIPTS_ROOT = Path("scripts")

def audit_drift():
    print("⚖️  Running GOV-04: Registry Drift Audit (Canonical Mode)...")
    
    if not REGISTRY_PATH.exists():
        # Fallback para local antigo se a migração não foi concluída
        REGISTRY_PATH_OLD = Path("comunication/registry.xml")
        if REGISTRY_PATH_OLD.exists():
            print(f"⚠️  Usando registry legado em {REGISTRY_PATH_OLD}")
            registry_to_use = REGISTRY_PATH_OLD
        else:
            print(f"❌ Critical: Registry not found at {REGISTRY_PATH}")
            return 1
    else:
        registry_to_use = REGISTRY_PATH

    try:
        with open(registry_to_use, 'r', encoding='utf-8') as f:
            xml_content = f.read().strip()
        root = ET.fromstring(xml_content)
    except Exception as e:
        print(f"❌ Error parsing registry: {e}")
        return 1

    scripts_node = root.find("Scripts")
    if scripts_node is None:
        print("❌ Invalid Registry structure.")
        return 1

    drift_issues = []
    for script in scripts_node.findall("Script"):
        name = script.get("name")
        status = script.get("status")
        if status == "DEPRECATED":
            continue
            
        # Busca recursiva em /scripts
        found = any(SCRIPTS_ROOT.rglob(name))
        if not found:
            drift_issues.append(f"Script Missing in disk: {name}")

    if drift_issues:
        for issue in drift_issues:
            print(f"   ❌ {issue}")
        return 1
    
    print("✅ Registry is consistent with physical scripts.")
    return 0

if __name__ == "__main__":
    sys.exit(audit_drift())
