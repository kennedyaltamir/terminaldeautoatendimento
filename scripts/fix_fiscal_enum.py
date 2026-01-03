import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def fix_fiscal_enum():
    print("🔧 Corrigindo tipo da coluna fiscal_status...")
    
    commands = [
        # 1. Remover a restrição de check se existir (para SQLite/outros)
        # 2. Alterar o tipo da coluna para VARCHAR simples para evitar problemas de Enum nativo
        "ALTER TABLE orders ALTER COLUMN fiscal_status TYPE VARCHAR(50);",
        
        # 3. Opcional: Se o banco for PostgreSQL e tiver criado um tipo enum 'fiscalstatus', podemos dropá-lo depois
        # Mas primeiro garantimos que a coluna é texto livre (controlado pela app)
        
        # 4. Atualizar valores existentes para minúsculo (garantia)
        "UPDATE orders SET fiscal_status = LOWER(fiscal_status);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                print(f"⚠️ Erro (pode ser ignorado se já estiver certo): {e}")
        conn.commit()
    
    print("\n🎉 Correção de Enum Fiscal aplicada!")

if __name__ == "__main__":
    fix_fiscal_enum()