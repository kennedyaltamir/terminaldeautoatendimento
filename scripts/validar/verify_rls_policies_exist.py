# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 01:00:00
import sys
import os
import io
from sqlalchemy import text
# ==============================================================================
# 🛡️ RLS POLICY VERIFIER (Windows Safe)
# ==============================================================================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.getcwd())
try:
    from app.database import SessionLocal
except ImportError as e:
    print(f"CRITICAL: Failed to import app modules: {e}")
    sys.exit(1)
REPORT_FILE = "comunication/reports/RLS_POLICY_VERIFICATION.md"
TARGET_TABLES = ["orders", "products", "companies"]
def verify_policies():
    print("🔍 Verifying RLS Policies...")
    db = SessionLocal()
    report_lines = [
        "# RLS Policy Verification Report",
        f"**Date:** {os.times()}",
        "",
        "## Status Table",
        "| Table | RLS Active | Policy Name | Status |",
        "| :--- | :---: | :--- | :---: |"
    ]
    all_ok = True
    try:
        for table in TARGET_TABLES:
            rls_query = text(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table}'")
            rls_active = db.execute(rls_query).scalar()
            policy_query = text(f"SELECT polname FROM pg_policy WHERE polrelid = '{table}'::regclass AND polname = 'tenant_isolation_policy'")
            policy_exists = db.execute(policy_query).scalar()
            status = "✅" if rls_active and policy_exists else "❌"
            if not (rls_active and policy_exists):
                all_ok = False
            report_lines.append(f"| `{table}` | {rls_active} | `{policy_exists or 'MISSING'}` | {status} |")
            print(f"   - {table}: RLS={rls_active}, Policy={policy_exists} [{status}]")
        report_lines.append(f"\n## Verdict: {'PASS' if all_ok else 'FAIL'}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        report_lines.append(f"\n## Error\n`{str(e)}`")
        all_ok = False
    finally:
        db.close()
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        print(f"📄 Report saved to {REPORT_FILE}")
        sys.exit(0 if all_ok else 1)
if __name__ == "__main__":
    verify_policies()

