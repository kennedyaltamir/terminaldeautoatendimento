# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 19:30:00
import requests
import sys
import os

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import Company, Table
from app.core.security import create_access_token

BASE_URL = "http://localhost:8000/api"
ADMIN_EMAIL = "admin@mesaflow.com"

def diagnose_tables_route():
    print("🔍 Diagnosticando Rota de Mesas (Backend)...")
    db = SessionLocal()
    
    try:
        # 1. Verificar se existem mesas no banco
        company = db.query(Company).filter(Company.owner_email == ADMIN_EMAIL).first()
        if not company:
            print("❌ Empresa admin não encontrada.")
            return

        tables_count = db.query(Table).filter(Table.company_id == company.id).count()
        print(f"   Mesas encontradas no banco: {tables_count}")

        # 2. Testar Endpoint da API
        token = create_access_token(data={
            "sub": company.owner_email,
            "role": "owner",
            "account_type": "company",
            "company_id": str(company.id)
        })
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            res = requests.get(f"{BASE_URL}/admin/tables/dashboard", headers=headers)
            if res.status_code == 200:
                print(f"✅ API /admin/tables/dashboard: OK (200)")
                data = res.json()
                print(f"   Dados retornados: {len(data)} mesas")
            else:
                print(f"❌ API /admin/tables/dashboard: FALHA ({res.status_code})")
                print(f"   Erro: {res.text}")
        except Exception as e:
            print(f"❌ Erro de conexão com API: {e}")

    except Exception as e:
        print(f"❌ Erro no diagnóstico: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    diagnose_tables_route()
