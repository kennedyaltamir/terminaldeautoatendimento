import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine, Base
from app.models import WebhookSubscription

def update_webhooks_schema():
    print("🔌 Atualizando esquema para Webhooks de Saída...")

    try:
        # Cria a tabela se não existir
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'webhook_subscriptions' verificada/criada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar esquema: {e}")

if __name__ == "__main__":
    update_webhooks_schema()
