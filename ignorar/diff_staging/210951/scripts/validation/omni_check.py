# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:00:00
import subprocess
import sys
import time
from datetime import datetime

# ==============================================================================
# 🔥 MESAFLOW OMNI-CHECK (Total Regression Shield)
# ==============================================================================
# Este script executa TODOS os validadores do sistema simultaneamente.
# Se um falhar, o sistema é considerado INSTÁVEL.
# ==============================================================================

VALIDATORS = [
    ("Integridade Sistêmica", "python scripts/governance/system_integrity_check.py"),
    ("Segurança RLS", "python scripts/validar/verify_TASK-SEC-01.py"),
    ("Auditoria de Ambiente", "python scripts/setup/audit_env.py"),
    ("Cadeia de Ledger", "python scripts/tests/test_ledger_integrity.py"),
    ("Conectividade API", "python scripts/governance/inf_01_healthcheck.py"),
    ("Drift de Documentação", "python scripts/governance/gov_04_registry_drift.py")
]

def run_omni():
    print(f"🚀 Iniciando MesaFlow Omni-Check v1.0")
    print(f"📅 Data: {datetime.now().isoformat()}")
    print("-" * 50)
    
    failed = []
    for name, cmd in VALIDATORS:
        print(f"🔍 Verificando: {name}...", end=" ", flush=True)
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print("✅ PASS")
            else:
                print("❌ FAIL")
                failed.append((name, res.stderr or res.stdout))
        except Exception as e:
            print("💥 ERROR")
            failed.append((name, str(e)))

    print("-" * 50)
    if not failed:
        print("🏆 RESULTADO: SISTEMA 100% ESTÁVEL. PRONTO PARA DEPLOY.")
        sys.exit(0)
    else:
        print(f"🚨 RESULTADO: {len(failed)} FALHAS DETECTADAS!")
        for name, err in failed:
            print(f"\n--- Erro em: {name} ---")
            print(err[:500] + "...")
        sys.exit(1)

if __name__ == "__main__":
    run_omni()
