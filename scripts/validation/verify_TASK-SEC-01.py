
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 11:45:00
import sys
import os
import io
import uuid
from sqlalchemy import text

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())

try:
    from app.database import SessionLocal, engine
except ImportError as e:
    print(f"CRITICAL: Import fail: {e}")
    sys.exit(1)

REPORT_FILE = "governance/evidence/RLS_VALIDATION_REPORT.md"

def run_rls_audit():
    print("Shield: Initiating RLS Isolation Audit (Hardened v12)...")
    db = SessionLocal()
    success = True
    logs = []
    
    try:
        tenant_a = str(uuid.uuid4())
        tenant_b = str(uuid.uuid4())
        order_id = str(uuid.uuid4())
        
        # Admin setup
        db.execute(text("DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'mesaflow_app') THEN CREATE ROLE mesaflow_app WITH LOGIN PASSWORD 'test_pass'; END IF; END $$;"))
        db.execute(text("GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO mesaflow_app;"))
        db.execute(text("GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO mesaflow_app;"))
        
        db.execute(text("SET row_security = off"))
        sql_comp = "INSERT INTO companies (id, name, slug, owner_email, plan_tier, segment, is_active, payment_provider) VALUES (:id, :n, :s, :e, 'pro', 'gastro', true, 'none')"
        db.execute(text(sql_comp), {"id": tenant_a, "n": "A", "s": f"a-{tenant_a[:4]}", "e": f"a@{tenant_a[:4]}.com"})
        db.execute(text(sql_comp), {"id": tenant_b, "n": "B", "s": f"b-{tenant_b[:4]}", "e": f"b@{tenant_b[:4]}.com"})
        
        sql_ord = "INSERT INTO orders (id, company_id, total_amount, status, order_type, origin) VALUES (:id, :cid, 100, 'pending', 'takeout', 'mesaflow')"
        db.execute(text(sql_ord), {"id": order_id, "cid": tenant_a})
        db.commit()
        
        # Test 1: Cross-tenant breach
        with engine.connect() as conn:
            conn.execute(text("SET row_security = on"))
            conn.execute(text("SET ROLE mesaflow_app"))
            conn.execute(text(f"SET app.current_company_id = '{tenant_b}'"))
            res = conn.execute(text(f"SELECT count(*) FROM orders WHERE id = '{order_id}'")).scalar()
            if res > 0:
                msg = "FAIL: Lateral leak detected! Tenant B accessed A."
                success = False
            else:
                msg = "PASS: Isolation confirmed between tenants."
            print(f"   [Test 1] {msg}")
            logs.append(f"- {msg}")

        # Test 2: Legitimate access
        with engine.connect() as conn:
            conn.execute(text("SET row_security = on"))
            conn.execute(text("SET ROLE mesaflow_app"))
            conn.execute(text(f"SET app.current_company_id = '{tenant_a}'"))
            res = conn.execute(text(f"SELECT count(*) FROM orders WHERE id = '{order_id}'")).scalar()
            if res == 1:
                msg = "PASS: Authorized access functional."
            else:
                msg = "FAIL: RLS blocked legitimate owner."
                success = False
            print(f"   [Test 2] {msg}")
            logs.append(f"- {msg}")

    except Exception as e:
        print(f"CRITICAL: Execution error: {repr(e)}")
        logs.append(f"- Error: {repr(e)}")
        success = False
    finally:
        db.close()
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("# RLS Validation Report (Hardened v12)\n\n")
            f.write(f"**Result:** {'SUCCESS' if success else 'FAILURE'}\n\n")
            f.write("## Logs\n")
            f.write("\n".join(logs))
            
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(run_rls_audit())

