import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import Lead

def update_leads_schema():
    print("🔧 Atualizando esquema para Leads...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'leads' verificada/criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    update_leads_schema()