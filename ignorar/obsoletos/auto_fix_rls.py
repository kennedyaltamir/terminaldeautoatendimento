import os
import glob
import subprocess
import sys
import re
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DA MIGRATION DEFINITIVA (PL/pgSQL Idempotente)
# ==============================================================================

# Truque para evitar conflito de aspas triplas no Python
Q3 = '"""'

# Template da Migration
MIGRATION_TEMPLATE = f"""{Q3}rls automagic fix

Revision ID: 20260108_9999
Revises: {{DOWN_REVISION}}
Create Date: 2026-01-08 12:00:00.000000

{Q3}
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260108_9999'
down_revision = {{DOWN_REVISION_STR}}
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Script PL/pgSQL Blindado
    
    rls_script = {Q3}
    DO $$
    DECLARE
        t text;
        target_tables text[] := ARRAY[
            'orders', 'products', 'tables', 'employees', 'categories', 
            'ingredients', 'table_sessions', 'service_requests', 
            'customer_wallets', 'audit_logs', 'service_fee_ledger', 
            'driver_ledger', 'order_feedbacks', 'webhook_subscriptions', 
            'feature_flags', 'promotions'
        ];
    BEGIN
        FOREACH t IN ARRAY target_tables LOOP
            -- Verifica se a tabela existe no schema public
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = t AND table_schema = 'public') THEN
                
                -- 1. Garantir company_id
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = t AND column_name = 'company_id' AND table_schema = 'public'
                ) THEN
                    RAISE NOTICE 'Adicionando company_id em %', t;
                    EXECUTE format('ALTER TABLE %I ADD COLUMN company_id UUID', t);
                    EXECUTE format('CREATE INDEX IF NOT EXISTS idx_%I_company_id ON %I (company_id)', t, t);
                END IF;

                -- 2. Habilitar RLS
                EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', t);
                EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', t);

                -- 3. Limpar Policy Antiga
                EXECUTE format('DROP POLICY IF EXISTS tenant_isolation_policy ON %I', t);

                -- 4. Criar Policy Fail-Secure
                -- Se app.current_company_id for vazio/null, nullif retorna NULL.
                -- company_id = NULL é FALSE. Acesso negado.
                EXECUTE format('
                    CREATE POLICY tenant_isolation_policy ON %I
                    AS PERMISSIVE
                    FOR ALL
                    TO public
                    USING (company_id = nullif(current_setting(''app.current_company_id'', true), '''') :: uuid)
                    WITH CHECK (company_id = nullif(current_setting(''app.current_company_id'', true), '''') :: uuid)
                ', t);
                
                RAISE NOTICE 'RLS aplicado em %', t;
            END IF;
        END LOOP;
    END $$;
    {Q3}
    op.execute(rls_script)

def downgrade() -> None:
    op.execute("RAISE NOTICE 'Downgrade de RLS não implementado automaticamente para segurança.';")
"""

def main():
    print("🚀 INICIANDO PROTOCOLO DE CORREÇÃO AUTOMÁTICA DE RLS...")
    
    base_dir = os.getcwd()
    versions_dir = os.path.join(base_dir, "alembic", "versions")
    
    if not os.path.exists(versions_dir):
        print(f"❌ Diretório {versions_dir} não encontrado.")
        sys.exit(1)

    # 1. LIMPEZA DE MIGRATIONS QUEBRADAS
    print("\n🧹 1. Varrendo migrations conflitantes...")
    files = glob.glob(os.path.join(versions_dir, "*.py"))
    
    deleted_count = 0
    remaining_files = []
    
    for f in files:
        filename = os.path.basename(f)
        # Removemos qualquer coisa que pareça ser as tentativas anteriores de RLS
        if "rls" in filename.lower() or "enable_rls" in filename or "add_company_id" in filename:
            try:
                os.remove(f)
                print(f"   🗑️  Removido: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"   ⚠️  Erro ao remover {filename}: {e}")
        else:
            remaining_files.append(f)
            
    print(f"   Total removido: {deleted_count}")

    # 2. DETERMINAR DOWN_REVISION
    print("\n🔗 2. Calculando árvore de dependência...")
    down_revision = None
    down_revision_str = "None"
    
    if remaining_files:
        remaining_files.sort()
        last_file = remaining_files[-1]
        try:
            with open(last_file, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"revision\s*=\s*['\"](.*?)['\"]", content)
                if match:
                    down_revision = match.group(1)
                    down_revision_str = f"'{down_revision}'"
                    print(f"   Base encontrada: {down_revision} ({os.path.basename(last_file)})")
        except Exception:
            pass
    else:
        print("   Nenhuma migration anterior encontrada. Assumindo base limpa.")

    # 3. GERAR NOVA MIGRATION
    print("\n📝 3. Escrevendo Migration Definitiva...")
    new_migration_path = os.path.join(versions_dir, "20260108_9999_rls_automagic.py")
    
    final_content = MIGRATION_TEMPLATE.format(
        DOWN_REVISION=down_revision if down_revision else "None",
        DOWN_REVISION_STR=down_revision_str
    )
    
    with open(new_migration_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"   ✅ Criado: {os.path.basename(new_migration_path)}")

    # 4. APLICAR NO BANCO
    print("\n⚙️  4. Executando Alembic Upgrade...")
    
    try:
        # Tenta upgrade direto
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"   ❌ Erro no upgrade:\n{result.stderr}")
            print("   Tentando 'alembic stamp head' para sincronizar e depois upgrade...")
            
            # Stamp head força o banco a aceitar que está atualizado (útil se o banco já tem a tabela alembic_version suja)
            subprocess.run(["alembic", "stamp", "head"], check=True)
            
            # Se tínhamos uma base, stamp nela e upgrade para garantir que o SQL rode
            if down_revision:
                print(f"   Resetando para {down_revision} e reaplicando...")
                subprocess.run(["alembic", "stamp", down_revision], check=True)
                subprocess.run(["alembic", "upgrade", "head"], check=True)
            else:
                subprocess.run(["alembic", "stamp", "base"], check=True)
                subprocess.run(["alembic", "upgrade", "head"], check=True)
                
        print("   ✅ Upgrade concluído.")
    except Exception as e:
        print(f"   💥 Falha crítica no Alembic: {e}")
        sys.exit(1)

    print("\n✨ PROCESSO AUTOMÁTICO FINALIZADO.")

if __name__ == "__main__":
    main()
