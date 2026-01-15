
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 00:15:00
import sys
import os
import io
from sqlalchemy import text

# ==============================================================================
# 🛡️ SECURE ROLE PROVISIONER
# ==============================================================================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())

try:
    from app.database import SessionLocal
except ImportError as e:
    print(f"CRITICAL: Failed to import app modules: {e}")
    sys.exit(1)

def provision_role():
    print("🔐 Provisioning Secure App Role...")
    db = SessionLocal()
    try:
        # Verifica se estamos rodando como superuser
        is_super = db.execute(text("SELECT usesuper FROM pg_user WHERE usename = current_user")).scalar()
        if not is_super:
            print("⚠️  WARNING: Current user is not a superuser. Role creation might fail.")

        # Cria a role se não existir
        db.execute(text("""
        DO $$
        BEGIN
          IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'mesaflow_app') THEN
            CREATE ROLE mesaflow_app WITH LOGIN PASSWORD 'mesaflow_secure_pass';
          END IF;
        END
        $$;
        """))
        
        # Garante permissões no schema public
        db.execute(text("GRANT USAGE ON SCHEMA public TO mesaflow_app"))
        db.execute(text("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mesaflow_app"))
        db.execute(text("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mesaflow_app"))
        db.execute(text("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mesaflow_app"))
        db.execute(text("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO mesaflow_app"))
        
        db.commit()
        print("✅ Role 'mesaflow_app' created/updated successfully.")
        print("   This role does NOT have BYPASSRLS permission.")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    provision_role()

