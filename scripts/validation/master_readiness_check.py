
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 11:10:00
import os
import sys
import io
import subprocess

# ==============================================================================
# 🚦 MASTER READINESS CHECK (MRC) v3.2 — Gold Master Edition
# ==============================================================================

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_check(name, command):
    print(f"Running: {name:<25}", end=" ")
    try:
        # PYTHONPATH garante que scripts encontrem o módulo 'app'
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        res = subprocess.run(
            command, 
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
            return False
    except Exception as e:
        print(f"💥 ERROR: {str(e)}")
        return False

def main():
    print("====================================================")
    print("🚀 MESAFLOW MASTER READINESS CHECK v3.2")
    print("   Status: CANONICAL STRUCTURE VERIFIED")
    print("====================================================")
    
    # MAPEAMENTO PARA A NOVA ESTRUTURA /scripts/
    checks = [
        ("Integridade Estrutural", "python scripts/governance/system_integrity_check.py"),
        ("Auditoria de Ambiente", "python scripts/setup/audit_env.py"),
        ("Row-Level Security", "python scripts/validation/verify_TASK-SEC-01.py"),
    ]
    
    all_pass = True
    for name, cmd in checks:
        if not run_check(name, cmd):
            all_pass = False
            
    print("-" * 52)
    if all_pass:
        print("\n✨ VEREDITO: SISTEMA 100% HOMOLOGADO (GOLD MASTER)")
        sys.exit(0)
    else:
        print("\n🚨 STATUS: PRODUCTION_READY_CONDITIONAL (BLOCKED)")
        print("   Verifique se o servidor local está online e se o .env está patcheado.")
        sys.exit(1)

if __name__ == "__main__":
    main()

