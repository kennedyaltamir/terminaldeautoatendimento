import os
import sys
from sqlalchemy import text
from pathlib import Path

# Ajuste de Path
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from app.database import SessionLocal
from app.models import Company

def check():
    print("🔍 Verificando prontidão do banco de dados para Mobile...")
    db = SessionLocal()
    try:
        admin = db.query(Company).filter(Company.owner_email == 'admin@mesaflow.com').first()
        if not admin:
            print("❌ ERRO: Usuário admin@mesaflow.com não encontrado no banco.")
            return

        print(f"✅ Usuário: {admin.owner_email}")
        print(f"✅ ID (UUID): {admin.id}")
        
        if not admin.id:
            print("❌ ERRO CRÍTICO: O usuário não possui um UUID. O Mobile vai rejeitar o login.")
        else:
            print("✅ Contexto Multi-tenant: OK")

    except Exception as e:
        print(f"💥 Erro na verificação: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check()
