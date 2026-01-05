import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def update_theme_schema():
    print("🎨 Atualizando esquema para Temas Personalizados...")
    
    commands = [
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS background_color VARCHAR(7) DEFAULT '#f9fafb';",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS text_color VARCHAR(7) DEFAULT '#111827';",
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS accent_color VARCHAR(7) DEFAULT '#ea580c';"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                # Ignora erro se a coluna já existir (para garantir idempotência)
                if "already exists" in str(e):
                    print(f"ℹ️  Coluna já existe.")
                else:
                    print(f"⚠️  Aviso: {e}")
        conn.commit()
    
    print("\n🎉 Banco de dados pronto para Personalização Visual!")

if __name__ == "__main__":
    update_theme_schema()