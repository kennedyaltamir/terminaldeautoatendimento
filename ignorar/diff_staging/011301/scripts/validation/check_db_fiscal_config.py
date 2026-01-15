# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 01:10:00
import sys
import os
import io
from sqlalchemy import text

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())
from app.database import SessionLocal

def check():
    print("🔍 Verificando persistência da configuração fiscal no Banco de Dados...")
    db = SessionLocal()
    try:
        # Busca a empresa principal
        query = text("SELECT name, cnpj, fiscal_token, inscricao_estadual FROM companies WHERE slug = 'hamburgueria-ze'")
        result = db.execute(query).fetchone()
        
        if not result:
            print("❌ Empresa 'hamburgueria-ze' não encontrada.")
            return 1
            
        name, cnpj, token, ie = result
        print(f"🏢 Empresa: {name}")
        print(f"🆔 CNPJ no DB: {cnpj}")
        print(f"📝 I.E. no DB: {ie}")
        print(f"🔑 Token no DB: {'********' + token[-4:] if token else 'AUSENTE'}")
        
        if not cnpj or not token:
            print("⚠️  AVISO: Dados fiscais incompletos no banco de dados.")
        else:
            print("✅ Dados persistidos corretamente no banco.")
            
        return 0
    except Exception as e:
        print(f"💥 Erro ao consultar banco: {e}")
        return 1
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(check())
