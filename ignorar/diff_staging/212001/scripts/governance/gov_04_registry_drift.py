# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:20:00
import os
import sys
import io
import xml.etree.ElementTree as ET
from pathlib import Path

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REGISTRY_PATH = Path("governance/registry.xml")
SCRIPTS_ROOT = Path("scripts")
EVIDENCE_DIR = Path("governance/evidence")

def audit_drift():
    print("⚖️  Running GOV-04: Registry Drift Audit...")
    if not REGISTRY_PATH.exists():
        print(f"❌ Critical: Registry not found at {REGISTRY_PATH}")
        return 1
    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            xml_content = f.read().strip()
        root = ET.fromstring(xml_content)
    except Exception as e:
        print(f"❌ Error parsing registry: {e}")
        return 1

    scripts_node = root.find("Scripts")
    drift_issues = []
    for script in scripts_node.findall("Script"):
        name = script.get("name")
        status = script.get("status")
        if status == "DEPRECATED": continue
        
        # Check physical existence
        found = any(SCRIPTS_ROOT.rglob(name))
        if not found:
            drift_issues.append(f"Script Missing: {name}")

    if drift_issues:
        for issue in drift_issues: print(f"   ❌ {issue}")
        return 1
    
    print("✅ Registry is consistent.")
    return 0

if __name__ == "__main__":
    sys.exit(audit_drift())
