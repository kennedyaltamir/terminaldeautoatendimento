
# DOMAIN: DATABASE
# LAST_MODIFIED: 2026-01-13 03:05:00
import sys
import os
import io
from sqlalchemy import text
# ==============================================================================
# 🛡️ MIGRATION VERIFIER (Windows Safe)
# ==============================================================================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.getcwd())
try:
    from app.database import SessionLocal
except ImportError as e:
    print(f"CRITICAL: Failed to import app modules: {e}")
    sys.exit(1)
REPORT_FILE = "comunication/reports/MIGRATION_VERIFICATION_REPORT.md"
def verify_rls_status(db):
    # Verifica se RLS está ativo nas tabelas críticas
    tables = ["orders", "products", "companies"]
    results = {}
    for t in tables:
        res = db.execute(text(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{t}'")).scalar()
        results[t] = res
    return results
def run_verification():
    print("🔍 Verifying Migrations Status...")
    db = SessionLocal()
    report_lines = [
        "# Migration Verification Report",
        f"**Date:** {os.times()}",
        "",
        "## RLS Status",
        "| Table | RLS Enabled |",
        "| :--- | :---: |"
    ]
    try:
        rls_status = verify_rls_status(db)
        all_ok = True
        for table, status in rls_status.items():
            icon = "✅" if status else "❌"
            report_lines.append(f"| `{table}` | {icon} {status} |")
            if not status:
                all_ok = False
                print(f"❌ RLS NOT enabled on {table}")
            else:
                print(f"✅ RLS enabled on {table}")
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
    run_verification()

