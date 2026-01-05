import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import AuditLog

def create_audit_table():
    print("🔧 Verificando e criando tabela de Auditoria...")
    
    # O create_all do SQLAlchemy é inteligente: só cria o que falta
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'audit_logs' verificada/criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    create_audit_table()