# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 00:10:00

import sys
import os
import io
from sqlalchemy import text

# ==============================================================================
# 🔍 SCHEMA DISCOVERY — SINGLE SOURCE OF TRUTH
# ==============================================================================

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.append(os.getcwd())

try:
    from app.database import SessionLocal
except ImportError as e:
    print(f"CRITICAL: Failed to import database session: {e}")
    sys.exit(1)

REPORT_FILE = "comunication/reports/SCHEMA_DISCOVERY_REPORT.md"

def discover_schema():
    print("🔍 Starting Schema Discovery...")
    db = SessionLocal()

    report = [
        "# Database Schema Discovery Report",
        "",
        "## Overview",
        "This report represents the **single source of truth** of the current database schema.",
        "",
        "## Tables Analysis",
        ""
    ]

    try:
        tables = db.execute(text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)).fetchall()

        if not tables:
            report.append("❌ No tables found in public schema.")
            raise RuntimeError("Empty schema detected.")

        for (table,) in tables:
            report.append(f"### Table: `{table}`")

            # Columns
            columns = db.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = :table
                ORDER BY ordinal_position;
            """), {"table": table}).fetchall()

            report.append("**Columns:**")
            for col, dtype in columns:
                report.append(f"- `{col}` : {dtype}")

            # company_id check
            has_company_id = any(col == "company_id" for col, _ in columns)
            report.append(f"- Has `company_id`: **{has_company_id}**")

            # RLS check
            rls = db.execute(text("""
                SELECT relrowsecurity
                FROM pg_class
                WHERE relname = :table;
            """), {"table": table}).scalar()

            report.append(f"- RLS Enabled: **{rls}**")

            # Policies
            policies = db.execute(text("""
                SELECT polname
                FROM pg_policy
                WHERE polrelid = :table::regclass;
            """), {"table": table}).fetchall()

            if policies:
                report.append("- Policies:")
                for (p,) in policies:
                    report.append(f"  - `{p}`")
            else:
                report.append("- Policies: **NONE**")

            report.append("")

        report.append("## Conclusion")
        report.append("This schema snapshot must be used for all subsequent migrations and security enforcement.")

    except Exception as e:
        report.append("## ERROR")
        report.append(f"`{str(e)}`")
        print(f"❌ ERROR: {e}")
    finally:
        db.close()
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        print(f"📄 Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    discover_schema()
