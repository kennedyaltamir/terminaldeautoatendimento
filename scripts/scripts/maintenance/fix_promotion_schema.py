import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine

def fix_promotion_schema():
    print("🔧 Corrigindo esquema de Promoções (UUID vs CHAR)...")

    with engine.connect() as conn:
        try:
            # 1. Remover a constraint antiga (se existir)
            conn.execute(text("ALTER TABLE orders DROP CONSTRAINT IF EXISTS fk_orders_promotion_id;"))
            
            # 2. Converter a coluna para UUID (com cast explícito)
            # O 'USING' é necessário para converter texto para UUID
            conn.execute(text("ALTER TABLE orders ALTER COLUMN promotion_id TYPE UUID USING promotion_id::uuid;"))
            
            # 3. Recriar a constraint correta
            conn.execute(text("""
                ALTER TABLE orders 
                ADD CONSTRAINT fk_orders_promotion_id 
                FOREIGN KEY (promotion_id) 
                REFERENCES promotions (id);
            """))
            
            conn.commit()
            print("✅ Coluna 'promotion_id' convertida para UUID e FK recriada.")
            
        except Exception as e:
            print(f"❌ Erro ao corrigir esquema: {e}")
            # Se falhar, pode ser que a coluna não exista ou já esteja certa.
            # Vamos tentar criar se não existir.
            try:
                conn.rollback()
                print("   Tentando criar coluna do zero...")
                conn.execute(text("ALTER TABLE orders ADD COLUMN IF NOT EXISTS promotion_id UUID;"))
                conn.execute(text("""
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
                """))
                conn.commit()
                print("✅ Coluna criada/verificada.")
            except Exception as e2:
                print(f"❌ Falha fatal: {e2}")

if __name__ == "__main__":
    fix_promotion_schema()
