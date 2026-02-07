"""rls automagic fix

Revision ID: 20260108_9999
Revises: None
Create Date: 2026-01-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260108_9999'
down_revision = '20260202_create_companies'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Script PL/pgSQL Blindado
    
    rls_script = """
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
    """
    op.execute(rls_script)

def downgrade() -> None:
    op.execute("RAISE NOTICE 'Downgrade de RLS não implementado automaticamente para segurança.';")
