# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 02:00:00
import sys
import os
import io
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.database import SessionLocal

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def audit_role_security():
    """
    SEC-01B: Auditoria de Roles e Privilégios.
    Garante que a role 'mesaflow_app' não possui bypass de RLS.
    """
    print("🔐 Auditando Roles de Aplicação...")
    db = SessionLocal()
    report_path = "comunication/reports/REPORT_SEC_01B.md"
    
    query = "SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = 'mesaflow_app';"
    
    try:
        role = db.execute(text(query)).fetchone()
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 🔐 Relatório de Matriz de Roles (SEC-01B)\n\n")
            if not role:
                f.write("❌ **FALHA:** Role `mesaflow_app` não encontrada no banco.\n")
                return False
            
            is_secure = not role.rolsuper and not role.rolbypassrls
            f.write(f"- Role: `{role.rolname}`\n")
            f.write(f"- Superuser: {'🔴 SIM' if role.rolsuper else '🟢 NÃO'}\n")
            f.write(f"- Bypass RLS: {'🔴 SIM' if role.rolbypassrls else '🟢 NÃO'}\n\n")
            f.write(f"**Veredito:** {'✅ SECURE' if is_secure else '❌ VULNERABLE'}")
            
        print(f"✅ Relatório gerado: {report_path}")
        return is_secure
    except Exception as e:
        print(f"❌ Erro na auditoria: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(0 if audit_role_security() else 1)
