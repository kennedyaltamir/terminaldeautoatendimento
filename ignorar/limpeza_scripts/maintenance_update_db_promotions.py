import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine, Base
from app.models import Promotion

def update_promotions_schema():
    print("🏷️ Atualizando esquema para Promoções e Cupons...")

    try:
        # 1. Criar Enum DiscountType se não existir
        with engine.connect() as conn:
            try:
                conn.execute(text("CREATE TYPE discounttype AS ENUM ('percentage', 'fixed', 'shipping');"))
                print("✅ Enum 'discounttype' criado.")
            except Exception:
                print("ℹ️  Enum 'discounttype' já existe.")
            conn.commit()

        # 2. Criar Tabela Promotions
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'promotions' verificada/criada.")

        # 3. Adicionar FK em Orders (se não existir)
        with engine.connect() as conn:
            commands = [
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS promotion_id CHAR(36);",
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_orders_promotion_id') THEN
                        ALTER TABLE orders
                        ADD CONSTRAINT fk_orders_promotion_id
                        FOREIGN KEY (promotion_id)
                        REFERENCES promotions (id);
                    END IF;
                END
                $$;
                """
            ]
            for cmd in commands:
                try:
                    conn.execute(text(cmd))
                except Exception as e:
                    print(f"⚠️ Aviso: {e}")
            conn.commit()
            print("✅ Coluna 'promotion_id' adicionada em 'orders'.")

    except Exception as e:
        print(f"❌ Erro crítico: {e}")

if __name__ == "__main__":
    update_promotions_schema()