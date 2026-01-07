import sys
import os
from sqlalchemy import text
from pathlib import Path

# Ajuste de Path para encontrar o app.database
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from app.database import engine

def fix_plantier_data():
    """
    Normaliza os dados da coluna plan_tier na tabela companies.
    Converte valores como 'PRO' para 'pro' para alinhar com o Enum do Python.
    """
    print("🚀 [SRE] Iniciando normalização de dados de PlanTier...")

    commands = [
        "UPDATE companies SET plan_tier = 'free' WHERE plan_tier = 'FREE';",
        "UPDATE companies SET plan_tier = 'pro' WHERE plan_tier = 'PRO';",
        "UPDATE companies SET plan_tier = 'enterprise' WHERE plan_tier = 'ENTERPRISE';"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                result = conn.execute(text(cmd))
                print(f"   ✅ Executado: {cmd} ({result.rowcount} linhas afetadas)")
            except Exception as e:
                print(f"   ⚠️ Erro ao executar '{cmd}': {str(e)[:100]}...")
        
        conn.commit()

    print("\n🎉 Normalização concluída! O erro de Enum deve estar resolvido.")

if __name__ == "__main__":
    fix_plantier_data()
