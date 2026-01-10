import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine, Base
from app.models import OrderFeedback

def update_feedback_schema():
    print("🔧 Atualizando esquema para Feedback (NPS)...")

    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'order_feedbacks' verificada/criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    update_feedback_schema()
