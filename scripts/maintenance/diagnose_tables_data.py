
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 15:10:00
import sys
import os
from sqlalchemy import text

# Adiciona a raiz ao path
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models import Company, Table

def diagnose():
    print("🔍 Diagnosticando Dados de Mesas...")
    db = SessionLocal()
    try:
        # Bypass RLS para ver a verdade nua e crua
        db.execute(text("SET row_security = off"))
        
        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        if not company:
            print("❌ Empresa 'hamburgueria-ze' não encontrada.")
            return

        print(f"🏢 Empresa: {company.name} (ID: {company.id})")
        
        tables = db.query(Table).filter(Table.company_id == company.id).all()
        print(f"📊 Total de Mesas: {len(tables)}")
        
        for t in tables:
            print(f"   - ID: {t.id} | Número: {t.table_number} | Token: {t.qr_token}")

    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    diagnose()

