import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import DriverLedger

def update_logistics_schema():
    print("🔧 Atualizando esquema de Logística (Driver Ledger)...")
    
    # O create_all do SQLAlchemy é inteligente: só cria o que falta
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'driver_ledger' verificada/criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    update_logistics_schema()