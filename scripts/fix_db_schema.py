import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def fix_schema():
    print("🔧 Atualizando esquema do banco de dados...")
    
    commands = [
        # Adiciona a coluna de saldo devedor se não existir (Empresas)
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS pending_commission_balance NUMERIC(10, 2) DEFAULT 0.00;",
        
        # Garante que a coluna de taxa também exista
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS marketplace_fee_percentage NUMERIC(5, 2) DEFAULT 0.00;",
        
        # NOVO: Adiciona a coluna driver_id na tabela orders
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS driver_id INTEGER;",
        
        # NOVO: Adiciona a chave estrangeira para employees (opcional, mas recomendado para integridade)
        # Usamos um bloco DO para verificar se a constraint já existe antes de criar
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
                print(f"✅ Executado com sucesso.")
            except Exception as e:
                print(f"⚠️ Erro ao executar comando: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados atualizado com sucesso!")

if __name__ == "__main__":
    fix_schema()