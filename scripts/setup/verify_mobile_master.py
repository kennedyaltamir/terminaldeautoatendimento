import subprocess
import sys

def run_all_verifications():
    scripts = [
        "scripts/setup/verify_mobile_missions_23_25.py",
        "scripts/setup/verify_mobile_mission_26.py",
        "scripts/setup/verify_mobile_mission_27.py",
        "scripts/setup/verify_mobile_mission_29a.py",
        "scripts/setup/verify_mobile_mission_29b.py",
        "scripts/setup/verify_mobile_mission_29c.py",
        "scripts/setup/verify_mobile_mission_30a.py",
        "scripts/setup/verify_mobile_mission_30b.py",
        "scripts/setup/verify_mobile_mission_31.py"
    ]
    
    print("🚀 INICIANDO AUDITORIA MESTRE DO ECOSSISTEMA MOBILE\n")
    
    failed = []
    for script in scripts:
        try:
            subprocess.check_call([sys.executable, script])
            print("-" * 40)
        except subprocess.CalledProcessError:
            failed.append(script)
            print("-" * 40)
            
    if not failed:
        print("\n🏆 TODAS AS MISSÕES ESTÃO INTEGRADAS E FUNCIONAIS!")
    else:
        print(f"\n🚨 FALHAS DETECTADAS EM: {len(failed)} missões.")
        for f in failed: print(f"  - {f}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_verifications()
