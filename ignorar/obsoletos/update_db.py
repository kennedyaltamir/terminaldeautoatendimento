import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_database_schema():
    print("🔧 Iniciando atualização do esquema do banco de dados...")
    
    commands = [
        # 1. Atualizações Financeiras (Fase 4.1)
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS pending_commission_balance NUMERIC(10, 2) DEFAULT 0.00;",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS marketplace_fee_percentage NUMERIC(5, 2) DEFAULT 0.00;",
        
        # 2. Atualizações de Logística/Delivery (Fase 4.2)
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS driver_id INTEGER;",
        
        # 3. Constraints (Chaves Estrangeiras)
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_orders_driver_id') THEN
                ALTER TABLE orders
                ADD CONSTRAINT fk_orders_driver_id
                FOREIGN KEY (driver_id)
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
                print(f"✅ Comando executado com sucesso.")
            except Exception as e:
                # Ignora erros de coluna já existente se o IF NOT EXISTS falhar em algumas versões do PG
                if "already exists" in str(e):
                    print(f"ℹ️  Coluna/Constraint já existe.")
                else:
                    print(f"⚠️  Aviso: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados atualizado e pronto para uso!")

if __name__ == "__main__":
    update_database_schema()