# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 02:30:00
import sys
import os
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.database import SessionLocal
def check_data_readiness():
    """
    DIAG-01: Data Readiness Check.
    Inspeciona o banco para verificar se há massa de dados mínima para testes funcionais.
    """
    print("🔍 Running DIAG-01: Data Readiness Check...")
    db = SessionLocal()
    checks = {
        "companies": "SELECT count(*) FROM companies",
        "orders": "SELECT count(*) FROM orders",
        "payment_transactions": "SELECT count(*) FROM payment_transactions",
        "employees": "SELECT count(*) FROM employees"
    }
    report = ["# 📊 Data Readiness Report\n"]
    all_ready = True
    for table, sql in checks.items():
        try:
            count = db.execute(text(sql)).scalar()
            status = "✅ READY" if count > 0 else "⚠️ EMPTY"
            if count == 0: all_ready = False
            report.append(f"- **{table}**: {count} records ({status})")
        except Exception as e:
            report.append(f"- **{table}**: ERROR ({str(e)})")
            all_ready = False
    report_path = "comunication/reports/REPORT_DIAG_01.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"✅ Report generated: {report_path}")
    return 0 if all_ready else 1
if __name__ == "__main__":
    sys.exit(check_data_readiness())