
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 11:45:00
import sys
import os
import uuid
import io
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.database import SessionLocal, engine

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_rls_test():
    """
    SEC-01: Validador de RLS Hardened v2.
    Corrige o erro de constraint e utiliza Role restrita para validar isolamento.
    """
    print("🛡️ Iniciando Teste de Isolamento RLS (Nível L6 - Hardened)...")
    db = SessionLocal()
    tenant_a = str(uuid.uuid4())
    tenant_b = str(uuid.uuid4())
    order_id = str(uuid.uuid4())
    
    try:
        # 1. Garantir que a role restrita existe (Setup inicial)
        db.execute(text("DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'mesaflow_app') THEN CREATE ROLE mesaflow_app WITH LOGIN PASSWORD 'mesaflow_pass'; END IF; END $$;"))
        db.execute(text("GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO mesaflow_app"))
        
        # 2. Setup de Dados (Como Superuser)
        print("   [1/3] Criando massa de dados para Tenant A...")
        sql_comp = """
            INSERT INTO companies (id, name, slug, owner_email, plan_tier, segment, payment_provider, is_active) 
            VALUES (:id, :name, :slug, :email, 'pro', 'gastro', 'none', true)
        """
        db.execute(text(sql_comp), {"id": tenant_a, "name": "Tenant A", "slug": f"a-{tenant_a[:4]}", "email": f"a@{tenant_a[:4]}.com"})
        db.execute(text(sql_comp), {"id": tenant_b, "name": "Tenant B", "slug": f"b-{tenant_b[:4]}", "email": f"b@{tenant_b[:4]}.com"})
        
        sql_order = """
            INSERT INTO orders (id, company_id, total_amount, status, customer_name, order_type, origin) 
            VALUES (:oid, :cid, 100, 'pending', 'Alvo RLS', 'dine_in', 'mesaflow')
        """
        db.execute(text(sql_order), {"oid": order_id, "cid": tenant_a})
        db.commit()
        
        # 3. Teste de Fogo (Como Tenant B usando Role Restrita)
        print("   [2/3] Tentando invasão lateral como Tenant B...")
        with engine.connect() as conn:
            # Força o uso da Role que obedece ao RLS
            conn.execute(text("SET ROLE mesaflow_app"))
            conn.execute(text("SET row_security = on"))
            # Tenta se passar pelo Tenant B
            conn.execute(text(f"SET app.current_company_id = '{tenant_b}'"))
            
            # Tenta ler o pedido do Tenant A
            count = conn.execute(text(f"SELECT count(*) FROM orders WHERE id = '{order_id}'")).scalar()
            
            if count > 0:
                print(f"❌ FALHA CRÍTICA: Tenant B conseguiu ler o pedido {order_id} do Tenant A!")
                return False
            
            print("   [3/3] Validando acesso legítimo do Tenant A...")
            conn.execute(text(f"SET app.current_company_id = '{tenant_a}'"))
            count_auth = conn.execute(text(f"SELECT count(*) FROM orders WHERE id = '{order_id}'")).scalar()
            
            if count_auth == 1:
                print("✅ SUCESSO: Isolamento RLS confirmado e funcional.")
                return True
            else:
                print("⚠️  AVISO: RLS bloqueou até o dono do dado. Verifique a Session Variable.")
                return False

    except Exception as e:
        print(f"🔥 Erro no teste: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = run_rls_test()
    sys.exit(0 if success else 1)

