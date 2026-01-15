import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def fix_tips_table():
    print("🔧 Criando tabela 'service_fee_ledger' manualmente...")
    
    commands = [
        """
        CREATE TABLE IF NOT EXISTS service_fee_ledger (
            id SERIAL PRIMARY KEY,
            company_id UUID NOT NULL REFERENCES companies(id),
            employee_id INTEGER NOT NULL REFERENCES employees(id),
            order_id UUID REFERENCES orders(id),
            amount NUMERIC(10, 2) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """,
        # Índice para performance
        "CREATE INDEX IF NOT EXISTS idx_ledger_employee ON service_fee_ledger (employee_id);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado com sucesso.")
            except Exception as e:
                print(f"⚠️ Erro ao executar comando: {e}")
        conn.commit()
    
    print("\n🎉 Tabela de gorjetas criada!")

if __name__ == "__main__":
    fix_tips_table()