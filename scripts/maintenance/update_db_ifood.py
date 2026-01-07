import sys
import os
from sqlalchemy import text
from pathlib import Path

# Ajuste de Path para encontrar o app.database
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from app.database import engine

def update_ifood_schema():
    print("🔧 Atualizando esquema do banco para integração iFood...")

    commands = [
        # 1. Criar o tipo ENUM para origem do pedido se não existir
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'orderorigin') THEN
                CREATE TYPE orderorigin AS ENUM ('mesaflow', 'ifood', 'rappi');
            END IF;
        END
        $$;
        """,

        # 2. Adicionar colunas na tabela de Empresas (Companies)
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS ifood_merchant_id VARCHAR(100);",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS ifood_token TEXT;",
        "CREATE INDEX IF NOT EXISTS idx_companies_ifood_merchant ON companies (ifood_merchant_id);",

        # 3. Adicionar colunas na tabela de Produtos (Products)
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS external_id VARCHAR(100);",
        "CREATE INDEX IF NOT EXISTS idx_products_external_id ON products (external_id);",

        # 4. Adicionar colunas na tabela de Pedidos (Orders)
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS origin orderorigin DEFAULT 'mesaflow';",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS external_order_id VARCHAR(100);",
        "CREATE INDEX IF NOT EXISTS idx_orders_external_id ON orders (external_order_id);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Comando executado com sucesso.")
            except Exception as e:
                print(f"⚠️ Aviso/Erro ao executar: {str(e)[:100]}...")
        
        conn.commit()

    print("\n🎉 Banco de dados sincronizado com o Middleware iFood!")

if __name__ == "__main__":
    update_ifood_schema()
