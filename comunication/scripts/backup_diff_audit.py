
# DOMAIN: DEVOPS
# LAST_MODIFIED: 2026-01-13 02:40:00
import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime
def audit_backups():
    """
    BKP-01: Backup Diff Audit (Refined).
    Realiza um diff estrutural entre os dois últimos snapshots para garantir rastreabilidade.
    """
    print("📦 Running BKP-01: Structural Backup Diff Audit...")
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("❌ Backup directory not found.")
        return 1
    zips = sorted(list(backup_dir.glob("*.zip")), key=os.path.getmtime)
    if len(zips) < 2:
        print(f"⚠️ Insufficient backups for diff (Found: {len(zips)}).")
        return 0 # Não bloqueia, mas avisa
    latest = zips[-1]
    previous = zips[-2]
    print(f"   Comparing: {previous.name} <-> {latest.name}")
    def get_zip_content(path):
        with zipfile.ZipFile(path, 'r') as z:
            return set(z.namelist())
    files_latest = get_zip_content(latest)
    files_previous = get_zip_content(previous)
    added = files_latest - files_previous
    removed = files_previous - files_latest
    report_path = "comunication/reports/REPORT_BKP_01.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📦 Backup Structural Diff Report (BKP-01)\n\n")
        f.write(f"- **Latest:** `{latest.name}`\n")
        f.write(f"- **Previous:** `{previous.name}`\n\n")
        f.write("## Changes Detected\n")
        f.write(f"- **Files Added:** {len(added)}\n")
        f.write(f"- **Files Removed:** {len(removed)}\n\n")
        if added:
            f.write("### ➕ Added\n")
            for a in sorted(list(added))[:10]: f.write(f"- `{a}`\n")
            if len(added) > 10: f.write("- ...\n")
        if removed:
            f.write("### ➖ Removed\n")
            for r in sorted(list(removed))[:10]: f.write(f"- `{r}`\n")
            if len(removed) > 10: f.write("- ...\n")
    print(f"✅ Diff report generated: {report_path}")
    return 0
if __name__ == "__main__":
    sys.exit(audit_backups())
