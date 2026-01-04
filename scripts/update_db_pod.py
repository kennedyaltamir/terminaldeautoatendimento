import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_pod_schema():
    print("🔧 Atualizando esquema para Proof of Delivery (POD)...")
    
    commands = [
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_code VARCHAR(4);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                print(f"⚠️  Aviso: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados atualizado para POD!")

if __name__ == "__main__":
    update_pod_schema()