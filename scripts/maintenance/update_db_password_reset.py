import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import PasswordResetToken

def update_password_reset_schema():
    print("🔧 Atualizando esquema para Recuperação de Senha...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'password_reset_tokens' verificada/criada com sucesso!")
        
        # Adicionar coluna is_email_verified na tabela companies se não existir
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE companies ADD COLUMN IF NOT EXISTS is_email_verified BOOLEAN DEFAULT FALSE;"))
            conn.commit()
            print("✅ Coluna 'is_email_verified' adicionada.")
            
    except Exception as e:
        print(f"❌ Erro ao atualizar esquema: {e}")

if __name__ == "__main__":
    update_password_reset_schema()