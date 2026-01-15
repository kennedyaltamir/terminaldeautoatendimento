
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 12:30:00
import sys
import os
import io
import uuid
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.database import SessionLocal

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def audit_effective_context():
    """
    SEC-01C: Validação de Propagação de Contexto.
    Verifica se a Session Variable é mantida no escopo da transação (LOCAL).
    """
    print("🧠 Auditando propagação de contexto de sessão...")
    db = SessionLocal()
    test_id = str(uuid.uuid4())
    report_path = "comunication/reports/REPORT_SEC_01C.md"
    
    try:
        # Define no escopo local da transação
        db.execute(text(f"SET LOCAL app.current_company_id = '{test_id}'"))
        current = db.execute(text("SELECT current_setting('app.current_company_id', true)")).scalar()
        
        success = (current == test_id)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 🧠 Relatório de Contexto Efetivo (SEC-01C)\n\n")
            f.write("Validação da variável de sessão necessária para o funcionamento do RLS.\n\n")
            f.write(f"- UUID Enviado: `{test_id}`\n")
            f.write(f"- UUID Detectado: `{current}`\n\n")
            f.write(f"**Veredito:** {'✅ PASS' if success else '❌ FAIL'}")
        
        print(f"✅ Relatório gerado: {report_path}")
        return success
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(0 if audit_effective_context() else 1)

