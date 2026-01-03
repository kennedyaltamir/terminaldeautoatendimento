import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_fiscal_ref():
    print("🔧 Atualizando esquema fiscal (Reference ID)...")
    
    commands = [
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS fiscal_reference_id VARCHAR(100);",
        "CREATE INDEX IF NOT EXISTS idx_orders_fiscal_ref ON orders (fiscal_reference_id);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                print(f"⚠️  Aviso: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados atualizado!")

if __name__ == "__main__":
    update_fiscal_ref()