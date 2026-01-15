
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 12:30:00
import sys
import os
import io
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.database import engine

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def audit_readonly_probe():
    """
    SEC-01D: Prova de Conceito de Filtro RLS via EXPLAIN.
    Garante que o plano de execução contenha o filtro de segurança.
    """
    print("🧪 Analisando Plano de Execução (Read-Only Probe)...")
    report_path = "comunication/reports/REPORT_SEC_01D.md"
    
    try:
        with engine.connect() as conn:
            # Ativa segurança na sessão
            conn.execute(text("SET row_security = on"))
            # Define um ID qualquer para forçar o filtro
            conn.execute(text("SET app.current_company_id = '00000000-0000-0000-0000-000000000000'"))
            
            # EXPLAIN VERBOSE para ver a expressão do filtro
            plan = conn.execute(text("EXPLAIN (VERBOSE, COSTS OFF) SELECT * FROM orders")).fetchall()
            plan_text = "\n".join([r[0] for r in plan])
            
            # Procura por referências ao isolamento de tenant no plano
            has_rls_filter = "app.current_company_id" in plan_text
            
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("# 🧪 Relatório de Prova Passiva RLS (SEC-01D)\n\n")
                f.write("Este teste prova que o PostgreSQL está injetando o filtro de segurança antes de tocar no disco.\n\n")
                f.write("## Plano de Execução Detectado\n")
                f.write(f"```sql\n{plan_text}\n```\n\n")
                f.write(f"**Veredito:** {'✅ PASS' if has_rls_filter else '❌ FAIL'}\n")
                f.write("\n> Nota: O sucesso aqui indica que o isolamento é estrutural e inegociável.")
            
            print(f"✅ Relatório gerado: {report_path}")
            return has_rls_filter
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if audit_readonly_probe() else 1)

