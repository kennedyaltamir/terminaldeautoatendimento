# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:55:00
import os
import subprocess
import sys
from pathlib import Path

def validate():
    print("Validando TASK-MOB-FIX-01 (Mobile Boot Capability)")
    
    # 1. Executa o Doctor usando o executável atual do Python
    print("Rodando Mobile Doctor")
    try:
        result = subprocess.run([sys.executable, "scripts/maintenance/mobile_doctor.py"], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("[ERRO] O Mobile Doctor reportou falhas ou falhou ao executar.")
            print("--- SAIDA DO DOCTOR ---")
            print(result.stdout)
            print(result.stderr)
            print("-----------------------")
            sys.exit(1)
        else:
            print("Mobile Doctor: [OK]")
    except Exception as e:
        print(f"[ERRO] Falha fatal ao tentar invocar o doctor: {e}")
        sys.exit(1)

    # 2. Verifica se o gerartxt.py está incluindo a pasta mobile
    print("Verificando inclusao da pasta mobile no contexto")
    if not Path("todososarquivos.txt").exists():
        print("[AVISO] todososarquivos.txt nao encontrado. Gere-o primeiro.")
    else:
        content = Path("todososarquivos.txt").read_text(encoding="utf-8", errors="ignore")
        if "[[MESAFLOW_BEGIN:mobile/App.tsx]]" not in content:
            print("[ERRO] A pasta mobile/ ainda esta sendo ignorada pelo gerartxt.py.")
            sys.exit(1)
        else:
            print("Inclusao de Contexto: [OK]")

    print("\nTASK-MOB-FIX-01 validada com sucesso.")
    sys.exit(0)

if __name__ == "__main__":
    validate()
