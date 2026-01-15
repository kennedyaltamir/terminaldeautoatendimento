
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 11:25:00
import sys
import os
import io
from sqlalchemy import text

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())
from app.database import SessionLocal

def discover():
    print("[SCHEMA] Initiating Schema Discovery and RLS Audit...")
    db = SessionLocal()
    
    tables_to_check = [
        "companies", "orders", "employees", "products", 
        "categories", "table_sessions", "financial_ledger"
    ]
    
    all_rls_enabled = True
    try:
        for table in tables_to_check:
            query = text(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table}'")
            res = db.execute(query).scalar()
            
            policy_query = text(f"SELECT count(*) FROM pg_policy WHERE polrelid = '{table}'::regclass")
            policy_count = db.execute(policy_query).scalar()
            
            if not res: 
                all_rls_enabled = False
            
            print(f"   Table {table:15}: RLS={'ACTIVE' if res else 'DISABLED'}, Policies={policy_count}")

        if not all_rls_enabled:
            print("\nWarning: RLS isolation is incomplete. Run 'apply_rls_migrations.py'.")
            return False
        
        print("\nSuccess: Database is compliant with isolation rules.")
        return True

    except Exception as e:
        print(f"\nError: Connection failure: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(0 if discover() else 1)

