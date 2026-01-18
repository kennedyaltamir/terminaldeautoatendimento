# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 16:40:00
import sys
import os
from sqlalchemy import text, create_engine

# Adiciona a raiz ao path
sys.path.append(os.getcwd())

try:
    from app.database import DATABASE_URL
except ImportError:
    print("❌ Erro ao importar configurações do banco.")
    sys.exit(1)

def fix_database():
    print("🔧 Iniciando reparo do banco de dados (Kiosk Column)...")
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 1. Verifica se a coluna existe
            print("   🔍 Verificando coluna 'kiosk_password_hash'...")
            check_sql = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='companies' AND column_name='kiosk_password_hash';
            """)
            result = conn.execute(check_sql).fetchone()
            
            if result:
                print("   ✅ Coluna já existe. Nenhuma ação necessária.")
            else:
                print("   ⚠️  Coluna ausente. Criando...")
                # Adiciona a coluna
                add_sql = text("ALTER TABLE companies ADD COLUMN kiosk_password_hash VARCHAR(255);")
                conn.execute(add_sql)
                conn.commit()
                print("   ✅ Coluna 'kiosk_password_hash' criada com sucesso.")
                
    except Exception as e:
        print(f"   ❌ Erro ao alterar banco: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(fix_database())

