
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 12:05:00
import sys
import os
import io
from sqlalchemy import text

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())

def robust_decode(error_obj):
    """Fallback decoder for Windows Postgres errors."""
    try:
        return str(error_obj)
    except UnicodeDecodeError:
        if hasattr(error_obj, 'args') and len(error_obj.args) > 0:
            raw_b = error_obj.args[1]
            if isinstance(raw_b, bytes):
                return raw_b.decode('cp1252', errors='replace')
    return repr(error_obj)

try:
    from app.database import SessionLocal
except ImportError:
    print("CRITICAL: Database module not found.")
    sys.exit(1)

RLS_MAP = {
    "companies": "id",
    "orders": "company_id",
    "employees": "company_id",
    "categories": "company_id",
    "ingredients": "company_id",
    "table_sessions": "company_id",
    "service_requests": "company_id",
    "customer_wallets": "company_id",
    "audit_logs": "company_id",
    "financial_ledger": "company_id",
    "payment_transactions": "company_id",
    "promotions": "company_id",
    "webhook_subscriptions": "company_id",
    "user_devices": "company_id",
    "suppliers": "company_id",
    "order_feedbacks": "company_id",
    "feature_flags": "company_id",
    "driver_ledger": "company_id",
    "service_fee_ledger": "company_id",
    "tables": "company_id",
    "products": "category_id IN (SELECT id FROM categories WHERE company_id = {ctx})",
    "order_items": "order_id IN (SELECT id FROM orders WHERE company_id = {ctx})",
    "option_groups": "product_id IN (SELECT p.id FROM products p JOIN categories c ON p.category_id = c.id WHERE c.company_id = {ctx})",
}

def apply_hardening():
    print("Shield: Initiating RLS Hardening L6...")
    try:
        db = SessionLocal()
        ctx_var = "nullif(current_setting('app.current_company_id', true), '')::uuid"
        
        for table, condition in RLS_MAP.items():
            print(f"   [+] Table: {table}")
            db.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;"))
            db.execute(text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY;"))
            db.execute(text(f"DROP POLICY IF EXISTS tenant_isolation_policy ON {table};"))
            formatted_condition = condition.format(ctx=ctx_var) if "{" in condition else f"{condition} = {ctx_var}"
            sql_policy = f"CREATE POLICY tenant_isolation_policy ON {table} AS PERMISSIVE FOR ALL TO public USING ({formatted_condition}) WITH CHECK ({formatted_condition});"
            db.execute(text(sql_policy))
        db.commit()
        print("Success: RLS Hardening applied.")
        db.close()
        return True
    except Exception as e:
        print(f"Error: Connection or SQL failure: {robust_decode(e)}")
        return False

if __name__ == "__main__":
    sys.exit(0 if apply_hardening() else 1)

