# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 01:00:00
import sys
import os
import io
from sqlalchemy import text
# ==============================================================================
# 🕵️ RLS CONTEXT INSPECTOR (Windows Safe)
# ==============================================================================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.getcwd())
try:
    from app.database import SessionLocal, set_tenant
except ImportError as e:
    print(f"CRITICAL: Failed to import app modules: {e}")
    sys.exit(1)
REPORT_FILE = "comunication/reports/RLS_CONTEXT_INSPECTION.md"
TARGET_TABLES = ["orders", "products", "companies"]
def inspect_rls():
    print("🔍 Starting RLS Context Inspection...")
    db = SessionLocal()
    report_lines = [
        "# RLS Context Inspection Report",
        f"**Date:** {os.times()}",
        "",
        "## 1. Database Configuration Check"
    ]
    try:
        print("   [1/3] Checking RLS Status on Tables...")
        report_lines.append("| Table | RLS Enabled | Policies |")
        report_lines.append("| :--- | :---: | :--- |")
        for table in TARGET_TABLES:
            rls_query = text(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table}'")
            rls_active = db.execute(rls_query).scalar()
            policy_query = text(f"SELECT polname FROM pg_policy WHERE polrelid = '{table}'::regclass")
            policies = [row[0] for row in db.execute(policy_query).fetchall()]
            policy_str = ", ".join(policies) if policies else "NONE"
            status_icon = "✅" if rls_active else "❌"
            report_lines.append(f"| `{table}` | {status_icon} {rls_active} | `{policy_str}` |")
            print(f"      - {table}: RLS={rls_active}, Policies={policy_str}")
        print("   [2/3] Checking Session Variable (Clean State)...")
        report_lines.append("\n## 2. Session Context Analysis")
        current_setting = db.execute(text("SELECT current_setting('app.current_company_id', true)")).scalar()
        report_lines.append(f"- **Initial Context:** `{current_setting}` (Expected: None/Null)")
        print(f"      - Initial: {current_setting}")
        print("   [3/3] Checking Session Variable (After set_tenant)...")
        test_uuid = "00000000-0000-0000-0000-000000000000"
        set_tenant(db, test_uuid)
        new_setting = db.execute(text("SELECT current_setting('app.current_company_id', true)")).scalar()
        report_lines.append(f"- **Context After Set:** `{new_setting}`")
        print(f"      - After Set: {new_setting}")
        if str(new_setting) == test_uuid:
            report_lines.append("\n### ✅ Context Propagation: SUCCESS")
        else:
            report_lines.append("\n### ❌ Context Propagation: FAILED")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        report_lines.append(f"\n## Error\n`{str(e)}`")
    finally:
        db.close()
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        print(f"📄 Report saved to {REPORT_FILE}")
if __name__ == "__main__":
    inspect_rls()
