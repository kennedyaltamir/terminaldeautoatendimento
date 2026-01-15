# DOMAIN: DATABASE
# LAST_MODIFIED: 2026-01-13 03:00:00
import sys
import os
import io
from sqlalchemy import text
from pathlib import Path
# ==============================================================================
# 🛡️ SQL MIGRATION APPLIER (Windows Safe)
# ==============================================================================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.getcwd())
try:
    from app.database import SessionLocal
except ImportError as e:
    print(f"CRITICAL: Failed to import app modules: {e}")
    sys.exit(1)
REPORT_FILE = "comunication/reports/SQL_MIGRATION_REPORT.md"
MIGRATIONS_DIR = Path("scripts/migrations")
def apply_sql_file(db, file_path):
    print(f"   📄 Applying: {file_path.name}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sql_content = f.read()
        # Executa o bloco SQL
        db.execute(text(sql_content))
        db.commit()
        return True, "Success"
    except Exception as e:
        db.rollback()
        return False, str(e)
def run_migrations():
    print("🚀 Starting SQL Migration Application...")
    db = SessionLocal()
    report_lines = [
        "# SQL Migration Report",
        f"**Date:** {os.times()}",
        "",
        "## Execution Log",
        "| File | Status | Message |",
        "| :--- | :---: | :--- |"
    ]
    success = True
    # Lista de arquivos SQL na ordem correta (pode ser melhorado com numeração)
    # Por enquanto, hardcoded para garantir a ordem crítica do RLS
    migration_order = [
        "enable_rls_core_tables.sql",
        "create_rls_policies.sql",
        "fix_rls_policies.sql" # Se existir
    ]
    for filename in migration_order:
        file_path = MIGRATIONS_DIR / filename
        if not file_path.exists():
            print(f"⚠️  Skipping {filename} (Not found)")
            continue
        ok, msg = apply_sql_file(db, file_path)
        status_icon = "✅" if ok else "❌"
        report_lines.append(f"| `{filename}` | {status_icon} | `{msg}` |")
        if not ok:
            success = False
            print(f"❌ Failed: {msg}")
            break # Para no primeiro erro
        else:
            print(f"✅ Applied: {filename}")
    report_lines.append(f"\n## Verdict: {'PASS' if success else 'FAIL'}")
    db.close()
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"📄 Report saved to {REPORT_FILE}")
    sys.exit(0 if success else 1)
if __name__ == "__main__":
    run_migrations()

