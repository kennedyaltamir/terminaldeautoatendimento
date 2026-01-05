import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_domains_schema():
    print("🔧 Atualizando esquema para Domínios Customizados...")
    
    commands = [
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS custom_domain VARCHAR(255);",
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_companies_custom_domain ON companies(custom_domain);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                print(f"⚠️  Aviso: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados pronto para White-Label!")

if __name__ == "__main__":
    update_domains_schema()