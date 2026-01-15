
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 11:25:00
import os
import sys
import io
import json
from pathlib import Path
from datetime import datetime

# Windows Resilience: Force UTF-8 Output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REPORT_PATH = Path("governance/evidence/REPORT_SYSTEM_INTEGRITY.md")
ERROR_LOG_PATH = Path("comunication/error.log")

def run_integrity_audit():
    # Removido emojis do print para evitar UnicodeEncodeError em terminais legados
    print("[SYS-01] Running System Integrity Audit...")
    
    required_paths = [
        "app", "frontend", "mobile", "scripts", 
        "governance/evidence", "governance/policies"
    ]
    
    issues = []
    results = []
    
    for p in required_paths:
        exists = Path(p).exists()
        status = "OK" if exists else "MISSING"
        if not exists:
            issues.append(f"Directory missing: {p}")
        results.append(f"| `{p}` | {'PASS' if exists else 'FAIL'} |")

    # Final Verdict
    success = (len(issues) == 0)
    
    report_content = [
        "# System Integrity Report (SYS-01)",
        f"**Date:** {datetime.now().isoformat()}",
        "\n## 1. Directory Verification",
        "| Path | Status |",
        "| :--- | :---: |",
        *results,
        f"\n## 2. Verdict: {'PASS' if success else 'FAIL'}"
    ]

    os.makedirs(REPORT_PATH.parent, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_content))

    if not success:
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "script": "SYS-01",
            "type": "INTEGRITY_FAILURE",
            "reason": "MISSING_DIRECTORIES",
            "details": issues
        }
        os.makedirs(ERROR_LOG_PATH.parent, exist_ok=True)
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_entry) + "\n")
        return 1

    print("Success: System structure is valid.")
    return 0

if __name__ == "__main__":
    sys.exit(run_integrity_audit())

