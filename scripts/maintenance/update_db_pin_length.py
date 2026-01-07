import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine

def update_pin_length():
    print("🔧 Atualizando comprimento do PIN de acesso para 10 dígitos...")

    commands = [
        # Altera o tipo da coluna para VARCHAR(10)
        "ALTER TABLE table_sessions ALTER COLUMN access_pin TYPE VARCHAR(10);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"✅ Executado: {cmd}")
            except Exception as e:
                print(f"⚠️ Erro ao atualizar coluna: {e}")
        conn.commit()

    print("\n🎉 Banco de dados atualizado para PINs de 10 dígitos!")

if __name__ == "__main__":
    update_pin_length()
