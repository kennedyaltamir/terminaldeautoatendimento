
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 04:10:00
import sys
import os
from sqlalchemy import text

# Adiciona a raiz ao path
sys.path.append(os.getcwd())
from app.database import SessionLocal

def fix_database_schema_and_data():
    print("🔧 Iniciando conversão de tipo e normalização de dados...")
    db = SessionLocal()
    try:
        # 1. Converte a coluna de ENUM nativo para VARCHAR (RFC-009 Hardening)
        # O 'USING' é obrigatório para converter tipos complexos no Postgres
        print("   [1/2] Convertendo coluna 'payment_provider' para VARCHAR...")
        db.execute(text("""
            ALTER TABLE companies 
            ALTER COLUMN payment_provider TYPE VARCHAR(50) 
            USING payment_provider::text
        """))
        
        # 2. Agora que é String, podemos normalizar para lowercase
        print("   [2/2] Normalizando valores para lowercase...")
        result = db.execute(text("""
            UPDATE companies 
            SET payment_provider = LOWER(payment_provider) 
            WHERE payment_provider IS NOT NULL
        """))
        
        db.commit()
        print(f"   ✅ Sucesso: Coluna convertida e {result.rowcount} registros normalizados.")
        
    except Exception as e:
        print(f"   ❌ Erro crítico na migração: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    fix_database_schema_and_data()

