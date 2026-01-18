# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 21:20:00
# ==============================================================================
# 🧼 MESAFLOW PURIFY & VERIFY ORCHESTRATOR
# ==============================================================================
# Objetivo: Automatizar a sequência de recuperação pós-colapso de confiança.
# ==============================================================================

import subprocess
import sys
import os
import io
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_step(name, cmd):
    print(f"\n--- [STEP] {name} ---")
    print(f"Running: {cmd}")
    try:
        # shell=True necessário para comandos npm/python no Windows
        result = subprocess.run(cmd, shell=True)
        if result.returncode == 0:
            print(f"✅ {name}: SUCCESS")
            return True
        else:
            print(f"❌ {name}: FAILED (Code: {result.returncode})")
            return False
    except Exception as e:
        print(f"💥 {name}: ERROR -> {e}")
        return False

def main():
    print("====================================================")
    print("🧼 MESAFLOW SYSTEMIC PURIFICATION PROTOCOL")
    print(f"Started at: {datetime.now().isoformat()}")
    print("====================================================")

    steps = [
        ("Meta-Audit (Pre-Check)", "python scripts/diagnostics/ultimate_systemic_auditor.py"),
        ("Frontend Compilation", "python scripts/validation/verify_frontend_compilation.py"),
        ("Kiosk Security Tests", "python scripts/automation/run_kiosk_tests.py"),
        ("System Integrity", "python scripts/governance/system_integrity_check.py")
    ]

    success_count = 0
    for name, cmd in steps:
        if run_step(name, cmd):
            success_count += 1
        else:
            print(f"\n🚨 CRITICAL FAILURE in {name}. Aborting sequence.")
            break

    print("\n" + "="*52)
    print(f"🏁 Sequence Finished. Success: {success_count}/{len(steps)}")
    if success_count == len(steps):
        print("🏆 SYSTEM RESTORED TO TRUSTED STATE.")
        sys.exit(0)
    else:
        print("🔴 SYSTEM STILL UNSTABLE. Check logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

