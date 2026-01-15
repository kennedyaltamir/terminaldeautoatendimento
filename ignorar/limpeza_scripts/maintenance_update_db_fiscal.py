import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_fiscal_schema():
    print("🔧 Atualizando esquema fiscal...")
    
    commands = [
        # Campos na Empresa
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS cnpj VARCHAR(20);",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS inscricao_estadual VARCHAR(20);",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS fiscal_token VARCHAR(255);",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS csc_token VARCHAR(100);",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS csc_id VARCHAR(10);",
        
        # Campos no Produto
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS ncm VARCHAR(10) DEFAULT '21069090';",
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS cfop VARCHAR(5) DEFAULT '5102';",
        
        # Campos no Pedido
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS fiscal_status VARCHAR(20) DEFAULT 'pending';",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS nfe_key VARCHAR(100);",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS nfe_url_xml VARCHAR(500);",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS nfe_url_pdf VARCHAR(500);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd[:50]}...")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"ℹ️  Já existe: {cmd[:30]}...")
                else:
                    print(f"⚠️  Erro: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados fiscal pronto!")

if __name__ == "__main__":
    update_fiscal_schema()