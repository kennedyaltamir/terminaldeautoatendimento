import sys
import os
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine

def migrate_payment_architecture():
    print("💳 Iniciando migração para Arquitetura Multi-Provedor...")
    
    with engine.connect() as conn:
        # 1. Criar Tipo Enum no Postgres (se não existir)
        try:
            conn.execute(text("CREATE TYPE paymentprovider AS ENUM ('mercadopago', 'efi', 'stripe', 'pagarme', 'none');"))
        except Exception:
            print("ℹ️  Enum paymentprovider já existe ou erro ignorável.")

        # 2. Adicionar Colunas
        commands = [
            "ALTER TABLE companies ADD COLUMN IF NOT EXISTS payment_provider VARCHAR(50) DEFAULT 'none';",
            "ALTER TABLE companies ADD COLUMN IF NOT EXISTS payment_credentials JSONB DEFAULT '{}'::jsonb;"
        ]
        
        for cmd in commands:
            try:
                conn.execute(text(cmd))
            except Exception as e:
                print(f"⚠️  Aviso na coluna: {e}")
        
        # 3. Migração de Dados (Legado -> Novo)
        print("🔄 Migrando tokens antigos para estrutura JSON...")
        
        # Migra quem tem Token MP
        conn.execute(text("""
            UPDATE companies 
            SET 
                payment_provider = 'mercadopago',
                payment_credentials = jsonb_build_object('access_token', mp_access_token)
            WHERE mp_access_token IS NOT NULL AND mp_access_token != '' AND payment_provider = 'none';
        """))
        
        # Migra quem tem apenas Pix Key (Modo Manual/None)
        # Mantemos provider 'none' mas salvamos a chave no json para uso futuro se criarmos um provider 'manual'
        conn.execute(text("""
            UPDATE companies 
            SET 
                payment_credentials = jsonb_build_object('pix_key', pix_key)
            WHERE pix_key IS NOT NULL AND pix_key != '' AND payment_credentials = '{}'::jsonb;
        """))

        conn.commit()
    
    print("✅ Migração Financeira Concluída!")

if __name__ == "__main__":
    migrate_payment_architecture()