
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 10:00:00
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# ==============================================================================
# 📜 SCRIPT INVENTORY AUDITOR (Omniscience Phase C)
# ==============================================================================
# Objetivo: Garantir que TODO script físico esteja catalogado no Registry.
# Detecta:
# 1. Orphans: Scripts que existem no disco mas não no XML.
# 2. Ghosts: Scripts que estão no XML mas não no disco.
# ==============================================================================

REGISTRY_PATH = Path("comunication/registry.xml")
SEARCH_DIRS = [
    Path("scripts"),
    Path("comunication/scripts")
]
IGNORE_DIRS = {
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    "tests" # Testes unitários geralmente não vão pro registry principal, mas podemos rever
}
IGNORE_FILES = {
    "__init__.py",
    "conftest.py"
}

def get_registered_scripts():
    if not REGISTRY_PATH.exists():
        return set()
    try:
        tree = ET.parse(REGISTRY_PATH)
        root = tree.getroot()
        return {s.get("name") for s in root.find("Scripts").findall("Script")}
    except:
        return set()

def get_physical_scripts():
    physical = set()
    for d in SEARCH_DIRS:
        for root, dirs, files in os.walk(d):
            # Filtrar diretórios ignorados
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file.endswith(".py") and file not in IGNORE_FILES:
                    physical.add(file)
    return physical

def audit():
    print("📜 Running Script Inventory Audit...")
    
    registered = get_registered_scripts()
    physical = get_physical_scripts()
    
    orphans = physical - registered
    ghosts = registered - physical
    
    # Remove ghosts que na verdade são scripts movidos/renomeados mas ainda úteis
    # (Ajuste fino pode ser necessário)
    
    print(f"   Registered: {len(registered)}")
    print(f"   Physical:   {len(physical)}")
    
    if orphans:
        print("\n🚨 ORPHAN SCRIPTS (Exist on disk, NOT in Registry):")
        for s in sorted(orphans):
            print(f"   - {s}")
            
    if ghosts:
        print("\n👻 GHOST SCRIPTS (Exist in Registry, NOT on disk):")
        for s in sorted(ghosts):
            print(f"   - {s}")
            
    if not orphans and not ghosts:
        print("\n✅ SCRIPT INVENTORY SYNCHRONIZED.")
        return 0
    else:
        print("\n❌ INVENTORY DRIFT DETECTED.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(audit())

