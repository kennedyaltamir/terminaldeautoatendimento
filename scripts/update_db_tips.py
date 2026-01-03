import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base

def update_tips_schema():
    print("🔧 Atualizando esquema de Gorjetas...")
    
    commands = [
        # Campos na Empresa
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS service_fee_percentage NUMERIC(5, 2) DEFAULT 10.00;",
        
        # Campos no Pedido
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS service_fee NUMERIC(10, 2) DEFAULT 0.00;",
        
        # Campos na Sessão
        "ALTER TABLE table_sessions ADD COLUMN IF NOT EXISTS opened_by_employee_id INTEGER;",
        
        # Constraints
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_sessions_employee_id') THEN
                ALTER TABLE table_sessions
                ADD CONSTRAINT fk_sessions_employee_id
                FOREIGN KEY (opened_by_employee_id)
                REFERENCES employees (id);
            END IF;
        END
        $$;
        """
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd[:50]}...")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"ℹ️  Já existe: {cmd[:30]}...")
                else:
                    print(f"⚠️  Erro: {e}")
        conn.commit()
    
    # Criar tabela nova (ServiceFeeLedger)
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'service_fee_ledger' verificada/criada!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

    print("\n🎉 Banco de dados de gorjetas pronto!")

if __name__ == "__main__":
    update_tips_schema()