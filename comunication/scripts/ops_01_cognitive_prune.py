# DOMAIN: DEVOPS | GOVERNANCE
# LAST_MODIFIED: 2026-01-13
# ID: OPS-01
# PURPOSE: Cognitive Noise Isolation (Non-Destructive)
import shutil
from pathlib import Path
from datetime import datetime
ROOT = Path(".")
IGNORE_DIR = ROOT / "ignorar"
LOG_DIR = ROOT / "comunication" / "logs"
REPORT_DIR = ROOT / "comunication" / "reports"
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
RUN_LOG = LOG_DIR / f"OPS_01_MOVE_LOG_{TIMESTAMP}.md"
# Regras de exclusão explícitas
MOVE_RULES = [
    ("comunication/logs", "*"),
    ("comunication/reports", "REPORT_*.md"),
    ("docs/tasks", "*"),
    ("docs/tasks/details", "*"),
    ("scripts", "sec_01_rls_integrity.py"),
    ("scripts", "verify_TASK-SEC-01.py"),
]
def ensure_dirs():
    IGNORE_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
def move_path(src: Path):
    relative = src.relative_to(ROOT)
    dest = IGNORE_DIR / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    return relative, dest.relative_to(ROOT)
def run():
    ensure_dirs()
    moved = []
    for base, pattern in MOVE_RULES:
        base_path = ROOT / base
        if not base_path.exists():
            continue
        for item in base_path.glob(pattern):
            if item.is_file():
                rel_src, rel_dest = move_path(item)
                moved.append((rel_src, rel_dest))
    with open(RUN_LOG, "w", encoding="utf-8") as f:
        f.write("# 🧹 OPS-01 — Cognitive Prune Log\n\n")
        f.write(f"- Timestamp: {TIMESTAMP} UTC\n")
        f.write(f"- Files moved: {len(moved)}\n\n")
        for src, dst in moved:
            f.write(f"- `{src}` → `{dst}`\n")
    print(f"✅ OPS-01 completed. Files moved: {len(moved)}")
    print(f"📄 Log: {RUN_LOG}")
if __name__ == "__main__":
    run()