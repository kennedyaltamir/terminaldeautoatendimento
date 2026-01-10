import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_whatsapp_schema():
    print("🔧 Adicionando campos de configuração de WhatsApp ao Banco...")
    
    commands = [
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS whatsapp_api_url VARCHAR(500);",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS whatsapp_instance VARCHAR(100);",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS whatsapp_token VARCHAR(500);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd[:40]}...")
            except Exception as e:
                print(f"⚠️ Aviso: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados pronto para notificações reais!")

if __name__ == "__main__":
    update_whatsapp_schema()
