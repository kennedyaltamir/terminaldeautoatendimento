# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11

import shutil
from pathlib import Path

ARCHIVE_ROOT = Path("archive/phase_10_hardening")
SCRIPTS_ARCHIVE = ARCHIVE_ROOT / "scripts"
DOCS_ARCHIVE = ARCHIVE_ROOT / "docs"

TO_ARCHIVE = [
    "scripts/validation/verify_TASK-ESC-01.py",
    "scripts/validation/verify_TASK-FIN-01.py",
    "scripts/validation/verify_TASK-MOB-01.py",
    "scripts/validation/verify_TASK-SEC-01.py",
    "scripts/security/verify_rls_public.py",

    "scripts/automation/enterprise_ui_explorer_v3.py",
    "scripts/automation/enterprise_ui_explorer_v4.py",
    "scripts/automation/enterprise_ui_explorer_v5.py",
    "scripts/automation/auto_fix_reporter.py",
    "scripts/automation/auto_fix_reporter_v2.py",
    "scripts/automation/auto_fix_reporter_v3.py",

    "scripts/setup/patch_ifood_secret.py",
    "scripts/setup/force_fix_env.py",

    "docs/tasks/details"
]

def prepare_handoff():
    print("📦 Preparando ambiente para handoff de IA...")

    SCRIPTS_ARCHIVE.mkdir(parents=True, exist_ok=True)
    DOCS_ARCHIVE.mkdir(parents=True, exist_ok=True)

    moved = 0

    for item in TO_ARCHIVE:
        src = Path(item)
        if not src.exists():
            continue

        dst = (
            SCRIPTS_ARCHIVE / src.name
            if "scripts" in src.parts
            else DOCS_ARCHIVE / src.name
        )

        try:
            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.move(str(src), str(dst))
            else:
                shutil.move(str(src), str(dst))

            print(f"   ↪️  Arquivado: {src}")
            moved += 1

        except Exception as e:
            print(f"   ⚠️  Falha ao arquivar {src}: {e}")

    print(f"\n✅ {moved} itens arquivados em {ARCHIVE_ROOT}")
    print("Contexto principal está limpo.")

if __name__ == "__main__":
    prepare_handoff()
