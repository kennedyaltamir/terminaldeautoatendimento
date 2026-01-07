import sys
import os
from pathlib import Path
from sqlalchemy import text

# Ajuste de Path para encontrar o app.database
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from app.database import engine, Base
from app.models import FeatureFlag # Garante que o model seja carregado

def update_features_schema():
    print("🔧 Criando tabela de Feature Flags no banco de dados...")

    try:
        # 1. Cria as tabelas que faltam baseadas nos models
        Base.metadata.create_all(bind=engine)
        print("✅ Tabela 'feature_flags' verificada/criada com sucesso.")

        # 2. Garante que o índice de performance existe
        with engine.connect() as conn:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_feature_flags_key ON feature_flags (key);"))
            conn.commit()
            print("✅ Índice de busca por chave verificado.")

    except Exception as e:
        print(f"❌ Erro ao atualizar esquema: {e}")

    print("\n🎉 Infraestrutura de Feature Flags pronta para uso!")

if __name__ == "__main__":
    update_features_schema()
