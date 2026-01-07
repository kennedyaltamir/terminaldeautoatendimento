import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine, Base
from app.models import UserDevice

def update_mobile_schema():
    print("📱 Atualizando esquema para App Nativo (User Devices)...")

    try:
        # Cria a tabela se não existir
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'user_devices' verificada/criada com sucesso!")
        
        # Verifica índice (opcional, o create_all já deve cuidar, mas reforçamos)
        with engine.connect() as conn:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_fcm_token ON user_devices (fcm_token);"))
            conn.commit()
            print("✅ Índice de token verificado.")

    except Exception as e:
        print(f"❌ Erro ao atualizar esquema: {e}")

if __name__ == "__main__":
    update_mobile_schema()
