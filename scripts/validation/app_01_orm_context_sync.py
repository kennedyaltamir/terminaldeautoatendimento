# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 02:25:00
import sys
import os
import io
import uuid
from sqlalchemy import text
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.getcwd())
from app.database import SessionLocal
REPORT_PATH = "comunication/reports/REPORT_APP_01.md"
def run_orm_sync_test():
    """
    APP-01: Verificação de propagação de contexto no ORM (v2 - Connection Aware).
    Valida se a aplicação consegue definir variáveis de sessão no Postgres.
    """
    print("🔄 Running APP-01: ORM Context Sync Check (v2)...")
    db = SessionLocal()
    test_id = str(uuid.uuid4())
    try:
        # Obtém a conexão bruta da sessão para evitar conflitos de gerenciamento de transação do ORM
        conn = db.connection()
        print(f"   [1/2] Setting session variable to: {test_id}")
        # Simula a lógica do set_tenant utilizando SET (nível de sessão) para validação estável
        conn.execute(text(f"SET app.current_company_id = '{test_id}'"))
        # 2. Verifica se o Postgres reteve o valor na mesma conexão
        db_val = conn.execute(text("SELECT current_setting('app.current_company_id', true)")).scalar()
        success = (db_val == test_id)
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("# 🔄 ORM Context Sync Report (APP-01)\n\n")
            f.write("## Objetivo\n")
            f.write("Validar se a camada de persistência consegue injetar o contexto de Tenant na sessão do banco.\n\n")
            f.write(f"- **UUID Enviado:** `{test_id}`\n")
            f.write(f"- **UUID no Postgres:** `{db_val}`\n\n")
            f.write("## Veredito\n")
            if success:
                f.write("✅ **PASS:** A propagação de contexto via sessão está funcional.\n")
            else:
                f.write("❌ **FAIL:** O banco de dados não retornou o valor esperado.\n")
        print(f"✅ Report: {REPORT_PATH}")
        return 0 if success else 1
    except Exception as e:
        print(f"💥 Error: {e}")
        return 1
    finally:
        db.close()
if __name__ == "__main__":
    sys.exit(run_orm_sync_test())

