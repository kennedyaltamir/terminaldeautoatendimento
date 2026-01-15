# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 03:10:00
import os
import shutil
from pathlib import Path
# ==============================================================================
# 🧹 SCRIPT ORGANIZER (Governance Enforcement)
# ==============================================================================
# Move scripts para a estrutura oficial de validação.
# ==============================================================================
ROOT = Path(".")
SCRIPTS_DIR = ROOT / "scripts"
VALIDAR_DIR = SCRIPTS_DIR / "validar"
VALIDADOS_DIR = SCRIPTS_DIR / "validados"
# Scripts que devem ser movidos para validar/ (se existirem nas pastas antigas)
TARGETS = [
    "discover_schema.py",
    "apply_rls_migrations.py",
    "verify_TASK-SEC-01.py",
    "inspect_rls_context.py",
    "verify_rls_policies_exist.py",
    "audit_env.py",
    "system_integrity_check.py",
    "reconcile_payments.py",
    "seed.py",
    "mobile_production_gate.py",
    "enterprise_ui_explorer_v5_1.py",
    "verify_governance_structure.py",
    "otimizar.py",
    "master_readiness_check.py"
]
def organize():
    print("🗂️  Organizing Scripts into Governance Structure...")
    VALIDAR_DIR.mkdir(parents=True, exist_ok=True)
    VALIDADOS_DIR.mkdir(parents=True, exist_ok=True)
    moved_count = 0
    # Procura em subpastas de scripts/ (maintenance, validation, security, etc)
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        # Pula as próprias pastas de destino para evitar loop
        if "validar" in root or "validados" in root:
            continue
        for file in files:
            if file in TARGETS:
                src = Path(root) / file
                dst = VALIDAR_DIR / file
                try:
                    shutil.move(str(src), str(dst))
                    print(f"   📦 Moved: {file} -> scripts/validar/")
                    moved_count += 1
                except Exception as e:
                    print(f"   ❌ Failed to move {file}: {e}")
    print(f"✨ Organization complete. {moved_count} scripts moved to validation queue.")
if __name__ == "__main__":
    organize()
