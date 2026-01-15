
import os
import sys
from pathlib import Path

# ==============================================================================
# MESAFLOW GOVERNANCE AUDITOR v1.0
# ==============================================================================

GOVERNANCE_ROOT = "docs/governance"

# Baseline de arquivos obrigatorios conforme especificacao
EXPECTED_BASELINE = {
    "DEFINITION_OF_DONE.md",
    "TASK_CHECKLIST_TEMPLATE.md",
    "README.md",
    "RFC/RFC-001.md",
    "RFC/RFC-002.md",
    "RFC/RFC-003.md",
    "RFC/RFC-004.md",
    "RFC/RFC-005.md",
    "RFC/RFC-006.md",
    "RFC/RFC-007.md",
    "RFC/RFC-008.md",
    "RFC/RFC-009.md",
    "RFC/RFC-010.md",
    "policies/enum_lifecycle.md",
    "policies/deprecation_policy.md",
}

def print_tree(directory: Path, prefix: str = ""):
    """Gera visualizacao da arvore de diretorios em ASCII."""
    if not directory.exists():
        print(f"[ERROR] Directory not found: {directory}")
        return

    items = sorted(list(directory.iterdir()))
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item.name}")
        if item.is_dir():
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(item, new_prefix)

def run_audit():
    print("------------------------------------------------------------")
    print("MESAFLOW GOVERNANCE AUDIT START")
    print("Target: " + GOVERNANCE_ROOT)
    print("------------------------------------------------------------")

    root_path = Path(GOVERNANCE_ROOT)
    
    if not root_path.exists():
        print("[FATAL] Governance root directory missing.")
        sys.exit(1)

    print("CURRENT STRUCTURE:")
    print(GOVERNANCE_ROOT + "/")
    print_tree(root_path)
    print("------------------------------------------------------------")

    # Coleta arquivos reais (relativos ao docs/governance)
    actual_files = set()
    for path in root_path.rglob("*"):
        if path.is_file():
            # Converte para path relativo ao docs/governance usando forward slashes
            rel_path = path.relative_to(root_path).as_posix()
            actual_files.add(rel_path)

    missing_files = sorted(list(EXPECTED_BASELINE - actual_files))
    extra_files = sorted(list(actual_files - EXPECTED_BASELINE))

    print("AUDIT REPORT:")
    print(f"Total Expected: {len(EXPECTED_BASELINE)}")
    print(f"Total Found:    {len(actual_files)}")
    
    status = "SUCCESS"
    exit_code = 0

    if missing_files:
        print("\nMISSING FILES DETECTED:")
        for f in missing_files:
            print(f"  [MISSING] {GOVERNANCE_ROOT}/{f}")
        status = "FAILED"
        exit_code = 1

    if extra_files:
        print("\nUNEXPECTED FILES DETECTED (DRIFT):")
        for f in extra_files:
            print(f"  [EXTRA]   {GOVERNANCE_ROOT}/{f}")
        # Extra files do not necessarily fail the audit, but are reported.
        # If strict enforcement is required, change exit_code to 1 here.

    print("------------------------------------------------------------")
    print(f"FINAL STATUS: {status}")
    print("------------------------------------------------------------")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    run_audit()

