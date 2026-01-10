# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:00:00
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    except Exception as e:
        return None

def fix():
    print("🛡️ MesaFlow Emulator Force Fixer")
    print("=================================")

    # 1. Matar Processos Zumbis
    print("\n[1/3] Matando processos zumbis (Emulator/QEMU)")
    if sys.platform == "win32":
        run_command("taskkill /F /IM emulator.exe")
        run_command("taskkill /F /IM qemu-system-x86_64.exe")
        run_command("taskkill /F /IM qemu-system-armel.exe")
    else:
        run_command("pkill -9 emulator")
        run_command("pkill -9 qemu-system")
    print("✅ Processos limpos.")

    # 2. Remover Arquivos de Trava (.lock)
    print("\n[2/3] Procurando arquivos .lock órfãos")
    home = Path.home()
    avd_path = home / ".android" / "avd"
    
    found_locks = False
    if avd_path.exists():
        for lock_file in avd_path.rglob("*.lock"):
            try:
                print(f"🗑️ Removendo trava: {lock_file}")
                if lock_file.is_file():
                    lock_file.unlink()
                elif lock_file.is_dir():
                    import shutil
                    shutil.rmtree(lock_file)
                found_locks = True
            except Exception as e:
                print(f"⚠️ Não foi possível remover {lock_file.name}: {e}")
    
    if not found_locks:
        print("ℹ️ Nenhuma trava encontrada.")
    else:
        print("✅ Travas removidas.")

    # 3. Sugestão de Comando de Boot Seguro
    print("\n[3/3] Diagnóstico concluído.")
    print("=================================")
    print("🚀 TENTE RODAR ESTE COMANDO AGORA:")
    print("emulator -avd Medium_Phone_API_36.1 -no-snapshot-load -gpu host")
    print("\nSe a tela continuar preta, tente o modo de segurança gráfica:")
    print("emulator -avd Medium_Phone_API_36.1 -no-snapshot-load -gpu angle_indirect")
    print("=================================")

if __name__ == "__main__":
    fix()
