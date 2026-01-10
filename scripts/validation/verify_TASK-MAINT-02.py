# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 02:30:00
import subprocess
import sys
from pathlib import Path

def validate():
    print("🔍 Validando TASK-MAINT-02 (Integrity Tool)")
    
    script_path = Path("scripts/maintenance/system_integrity_check.py")
    if not script_path.exists():
        print("❌ ERRO: Script AIS não encontrado.")
        exit(1)
        
    # Tenta rodar o script. Como o sistema está funcional, deve retornar 0 ou 1 (se houver avisos)
    # mas não deve dar crash de Python.
    try:
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        if "MesaFlow System Integrity Auditor" in result.stdout:
            print("✅ Ferramenta de auditoria validada com sucesso.")
            exit(0)
        else:
            print("❌ ERRO: Saída da ferramenta inesperada.")
            exit(1)
    except Exception as e:
        print(f"❌ ERRO ao executar auditoria: {e}")
        exit(1)

if __name__ == "__main__":
    validate()
