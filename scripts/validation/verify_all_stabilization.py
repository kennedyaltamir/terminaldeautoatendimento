# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:58:00
import subprocess
import sys

def run_script(name, path):
    print(f"\n--- Executando: {name} ---")
    result = subprocess.run([sys.executable, path])
    return result.returncode == 0

def main():
    print("🚀 Iniciando Suite de Verificacao de Estabilizacao (Enterprise Revamp)")
    
    tasks = [
        ("Sanitizacao (MAINT-01)", "scripts/validation/verify_TASK-MAINT-01.py"),
        ("Ambiente (ENV-01)", "scripts/validation/verify_TASK-ENV-01.py"),
        ("Documentacao (DOC-01)", "scripts/validation/verify_TASK-DOC-01.py"),
        ("Mobile Boot (MOB-FIX-01)", "scripts/validation/verify_TASK-MOB-FIX-01.py"),
        ("Mobile Screens (MOB-02)", "scripts/validation/verify_TASK-MOB-02.py"),
    ]
    
    success_count = 0
    for name, path in tasks:
        if run_script(name, path):
            success_count += 1
        else:
            print(f"❌ Falha na verificacao de {name}")
            
    print("\n" + "="*40)
    print(f"RESULTADO FINAL: {success_count}/{len(tasks)} Tasks Validadas")
    print("="*40)
    
    if success_count == len(tasks):
        print("✨ Sistema Estabilizado com Sucesso!")
        sys.exit(0)
    else:
        print("⚠️  Existem pendencias a serem corrigidas.")
        sys.exit(1)

if __name__ == "__main__":
    main()
