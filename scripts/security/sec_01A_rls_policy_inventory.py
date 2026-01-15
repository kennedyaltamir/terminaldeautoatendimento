
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 12:30:00
import sys
import os
import io
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.database import SessionLocal

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def audit_rls_policies():
    """
    SEC-01A: Auditoria de Existência e Força de Políticas RLS.
    Correção: Utiliza pg_class para verificar relrowsecurity e relforcerowsecurity.
    """
    print("🔎 Auditando políticas de banco de dados via pg_class (Read-Only)...")
    db = SessionLocal()
    report_path = "comunication/reports/REPORT_SEC_01A.md"
    
    # Query canônica para verificação de RLS no PostgreSQL
    query = """
    SELECT 
        c.relname AS tablename,
        c.relrowsecurity AS rowsecurity,
        c.relforcerowsecurity AS forcerowsecurity
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public' 
      AND c.relkind = 'r'
      AND c.relname IN ('orders', 'companies', 'employees', 'products');
    """
    
    try:
        results = db.execute(text(query)).fetchall()
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 🔎 Relatório de Inventário RLS (SEC-01A)\n\n")
            f.write("Este relatório valida se o motor do banco de dados está protegendo as tabelas core.\n\n")
            f.write("| Tabela | RLS Ativo | Forçado (FORCE) | Status |\n")
            f.write("| :--- | :---: | :---: | :---: |\n")
            
            all_pass = True
            for row in results:
                is_ok = row.rowsecurity and row.forcerowsecurity
                if not is_ok: all_pass = False
                f.write(f"| {row.tablename} | {'✅' if row.rowsecurity else '❌'} | {'✅' if row.forcerowsecurity else '❌'} | {'PASS' if is_ok else 'FAIL'} |\n")
            
            if not results:
                f.write("\n⚠️ **AVISO:** Nenhuma das tabelas alvo foi encontrada no schema público.\n")
                all_pass = False

            f.write(f"\n**Veredito:** {'✅ COMPLIANT' if all_pass else '❌ NON-COMPLIANT'}")
        
        print(f"✅ Relatório gerado: {report_path}")
        return all_pass
    except Exception as e:
        print(f"❌ Erro na auditoria: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(0 if audit_rls_policies() else 1)

