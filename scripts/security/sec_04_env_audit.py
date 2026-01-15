# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 02:30:00
import os
import sys
from pathlib import Path
def run_env_audit():
    """
    SEC-04: Secrets & Env Audit.
    Compara .env com .env.example e busca por placeholders perigosos.
    """
    print("🛡️ Running SEC-04: Secrets & Environment Audit...")
    env_path = Path(".env")
    example_path = Path(".env.example")
    report_path = Path("comunication/reports/REPORT_SEC_04.md")
    checks = []
    success = True
    if not env_path.exists():
        checks.append({"name": "File Existence", "status": "FAIL", "details": ".env file missing!"})
        success = False
    else:
        checks.append({"name": "File Existence", "status": "PASS", "details": ".env file found."})
        with open(env_path, 'r') as f:
            env_keys = {line.split('=')[0].strip() for line in f if '=' in line and not line.startswith('#')}
        with open(example_path, 'r') as f:
            example_keys = {line.split('=')[0].strip() for line in f if '=' in line and not line.startswith('#')}
        missing_keys = example_keys - env_keys
        if missing_keys:
            checks.append({"name": "Key Completeness", "status": "FAIL", "details": f"Missing keys: {', '.join(missing_keys)}"})
            success = False
        else:
            checks.append({"name": "Key Completeness", "status": "PASS", "details": "All keys from .env.example are present."})
        placeholders = ['changeme', 'your_', 'placeholder', 'sk_test', 'pk_test']
        found_placeholders = []
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, val = line.split('=', 1)
                    if any(p in val.lower() for p in placeholders):
                        found_placeholders.append(key.strip())
        if found_placeholders:
            checks.append({"name": "Production Readiness", "status": "WARN", "details": f"Placeholders or test keys found in: {', '.join(found_placeholders)}"})
        else:
            checks.append({"name": "Production Readiness", "status": "PASS", "details": "No placeholders detected."})
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🛡️ Secrets & Env Audit Report (SEC-04)\n\n")
        f.write("| Check | Status | Details |\n")
        f.write("| :--- | :---: | :--- |\n")
        for c in checks:
            f.write(f"| {c['name']} | {c['status']} | {c['details']} |\n")
        f.write(f"\n**Final Verdict:** {'✅ READY' if success else '❌ ACTION REQUIRED'}\n")
    print(f"✅ Report: {report_path}")
    return 0 if success else 1
if __name__ == "__main__":
    sys.exit(run_env_audit())
