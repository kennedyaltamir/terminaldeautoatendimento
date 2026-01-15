# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:30:00
import subprocess
import sys
import io
import os
from datetime import datetime

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 🔥 MESAFLOW OMNI-CHECK v1.2 (Ultra-Robust)
# ==============================================================================

VALIDATORS = [
    ("Integridade Sistêmica", "python scripts/governance/system_integrity_check.py"),
    ("Segurança RLS", "python scripts/security/sec_01_rls_integrity.py"),
    ("Auditoria de Ambiente", "python scripts/security/sec_04_env_audit.py"),
    ("Cadeia de Ledger", "python scripts/tests/test_ledger_integrity.py"),
    ("Conectividade API", "python scripts/governance/inf_01_healthcheck.py"),
    ("Drift de Documentação", "python scripts/governance/gov_04_registry_drift.py")
]

def run_omni():
    print("🚀 Iniciando MesaFlow Omni-Check v1.2")
    print(f"📅 Data: {datetime.now().isoformat()}")
    print("-" * 50)
    
    failed = []
    # Força o Python a usar UTF-8 para os processos filhos
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    for name, cmd in VALIDATORS:
        print(f"🔍 Verificando: {name}...", end=" ", flush=True)
        try:
            # shell=True é necessário no Windows para comandos 'python ...'
            res = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                errors='replace',
                env=env
            )
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
        print("🏆 RESULTADO: SISTEMA 100% ESTÁVEL.")
        sys.exit(0)
    else:
        print(f"🚨 RESULTADO: {len(failed)} FALHAS DETECTADAS!")
        for name, err in failed:
            print(f"\n--- Erro em: {name} ---")
            print(err[:1000])
        sys.exit(1)

if __name__ == "__main__":
    run_omni()
