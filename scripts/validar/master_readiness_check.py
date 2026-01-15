# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 12:40:00
import os
import sys
import io
import subprocess
from datetime import datetime

# ==============================================================================
# 🚦 MASTER READINESS CHECK (MRC) v3.5 — Gold Master Edition
# ==============================================================================
# Fix: Força o uso de UTF-8 no stdout para evitar crash com emojis no Windows.
# Fix: Inclusão de OBS-01 (Sentry) no loop de verificação.
# ==============================================================================

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_check(name, command):
    print(f"Running: {name:<30}", end=" ")
    try:
        # Define PYTHONPATH para garantir que scripts encontrem o módulo 'app'
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        res = subprocess.run(
            f"python {command}", 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='replace',
            env=env
        )
        
        if res.returncode == 0:
            print("✅ PASS")
            return True
        else:
            print("❌ FAIL")
            # Log do erro estruturado para o error.log
            os.makedirs("comunication/logs", exist_ok=True)
            with open("comunication/error.log", "a", encoding="utf-8") as f:
                f.write(f"\n--- FAIL: {name} ({datetime.now()}) ---\n")
                f.write(res.stdout + "\n" + res.stderr)
            return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def main():
    print("====================================================")
    print(f"MESAFLOW MASTER READINESS CHECK v3.5")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("====================================================")

    # MAPEAMENTO CANONICO DE SCRIPTS
    checks = [
        ("Integridade Estrutural (SYS-01)", "scripts/governance/system_integrity_check.py"),
        ("Auditoria de Ambiente (SEC-04)", "scripts/security/audit_env.py"),
        ("Descoberta de Schema", "scripts/validar/discover_schema.py"),
        ("Row-Level Security (SEC-01)", "scripts/validar/verify_TASK-SEC-01.py"),
        ("Observabilidade Sentry (OBS-01)", "scripts/observability/sentry_ingest_test.py"),
        ("Healthcheck API (INF-01)", "scripts/governance/inf_01_healthcheck.py")
    ]

    all_pass = True
    for name, cmd in checks:
        if not run_check(name, cmd):
            all_pass = False

    print("-" * 52)
    if all_pass:
        print("\n🏆 VEREDITO: SISTEMA 100% HOMOLOGADO PARA PRODUCAO.")
        sys.exit(0)
    else:
        print("\n🚨 STATUS: PRODUCTION_BLOCKED")
        print("   Consulte 'comunication/error.log' para detalhes.")
        sys.exit(1)

if __name__ == "__main__":
    main()

