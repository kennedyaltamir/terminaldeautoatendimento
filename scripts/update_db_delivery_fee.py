import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_delivery_fee_schema():
    print("🔧 Atualizando esquema para Taxas de Entrega...")
    
    commands = [
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS fixed_delivery_fee NUMERIC(10, 2) DEFAULT 0.00;",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_fee NUMERIC(10, 2) DEFAULT 0.00;"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                print(f"⚠️  Aviso: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados atualizado para Taxas de Entrega!")

if __name__ == "__main__":
    update_delivery_fee_schema()