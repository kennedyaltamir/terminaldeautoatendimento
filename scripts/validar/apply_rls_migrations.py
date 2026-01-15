
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 11:15:00
import sys
import os
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.database import SessionLocal

def apply():
    """
    Aplica as políticas de Row-Level Security (RLS) em massa.
    Garante o isolamento 'Zero-Leak' entre tenants.
    """
    print("🛡️  Iniciando Aplicação de Hardening RLS...")
    db = SessionLocal()
    
    # Lista de tabelas que exigem isolamento por company_id
    tables = [
        "orders", "categories", "products", "employees", 
        "table_sessions", "service_requests", "customer_wallets",
        "audit_logs", "financial_ledger", "payment_transactions",
        "promotions", "webhook_subscriptions", "user_devices", "suppliers"
    ]

    try:
        # 1. Habilitar RLS em todas as tabelas
        for table in tables:
            print(f"   -> Protegendo: {table}")
            db.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;"))
            db.execute(text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY;"))
            
            # 2. Criar Política Padrão (Isolamento via variável de sessão)
            # Nota: 'app.current_company_id' é setado no database.py durante a conexão
            db.execute(text(f"DROP POLICY IF EXISTS tenant_isolation_policy ON {table};"))
            
            if table == "companies":
                # A tabela companies é isolada pelo seu próprio ID
                sql = f"""
                CREATE POLICY tenant_isolation_policy ON {table}
                USING (id = nullif(current_setting('app.current_company_id', true), '')::uuid);
                """
            else:
                sql = f"""
                CREATE POLICY tenant_isolation_policy ON {table}
                USING (company_id = nullif(current_setting('app.current_company_id', true), '')::uuid);
                """
            db.execute(text(sql))
        
        db.commit()
        print("\n✅ Hardening L6 concluído com sucesso.")
        return True

    except Exception as e:
        print(f"\n🔥 FALHA CRÍTICA NA MIGRAÇÃO RLS: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    apply()

