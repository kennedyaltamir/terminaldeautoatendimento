# scripts/maintenance/move_noise_to_ignore.py
import shutil
from pathlib import Path

ROOT = Path(".")
IGNORE = ROOT / "ignorar"

CATEGORIES = {
    "reports_old": [
        "comunication/reports"
    ],
    "scripts_meta": [
        "scripts/automation",
        "scripts/l6",
        "scripts/maintenance",
        "scripts/collector",
        "scripts/verification",
    ],
    "frontend": ["frontend"],
    "mobile": ["mobile", "docs/mobile"],
    "docs_noise": [
        "docs/investors",
        "docs/commercial",
        "docs/management",
        "docs/strategy",
        "docs/team",
        "docs/archive",
        "docs/improvements",
        "docs/releases",
    ],
}

KEEP_REPORTS = {
    "REPORT_FINAL_STATUS_v3.md",
    "REPORT_PHASE_3_READINESS.md",
    "REPORT_READINESS_SUMMARY.md",
    "PIPELINE_CANONICO.md",
    "SCHEMA_DISCOVERY_REPORT.md",
    "RLS_VALIDATION_REPORT.md",
    "AUDIT_ENV_REPORT.md",
}

def ensure(p): p.mkdir(parents=True, exist_ok=True)

for category, paths in CATEGORIES.items():
    target = IGNORE / category
    ensure(target)

    for p in paths:
        src = ROOT / p
        if not src.exists():
            continue

        if "reports" in p:
            for file in src.glob("*.md"):
                if file.name not in KEEP_REPORTS:
                    shutil.move(str(file), target / file.name)
        else:
            shutil.move(str(src), target / src.name)

print("✅ Context noise movido para /ignorar")
