import sys
import os
from sqlalchemy import text
from pathlib import Path

# Ajuste de Path para encontrar o app.database
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from app.database import engine

def fix_audit_enum():
    """
    Atualiza o tipo ENUM 'auditaction' no PostgreSQL para incluir novos valores.
    Utiliza AUTOCOMMIT pois ALTER TYPE ADD VALUE não pode rodar em transação.
    """
    print("🔧 Sincronizando tipo ENUM 'auditaction' no PostgreSQL...")

    new_values = ['impersonate', 'feature_toggle']

    # Configura conexão para autocommit
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        for val in new_values:
            try:
                # Tenta adicionar o valor em minúsculo
                conn.execute(text(f"ALTER TYPE auditaction ADD VALUE '{val}';"))
                print(f"✅ Valor '{val}' adicionado com sucesso.")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"ℹ️  O valor '{val}' já existe no Enum.")
                else:
                    print(f"⚠️ Erro ao adicionar '{val}': {e}")

    print("\n🎉 Sincronização de Enums concluída!")

if __name__ == "__main__":
    fix_audit_enum()
