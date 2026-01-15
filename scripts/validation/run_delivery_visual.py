# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:00:00
import subprocess
import sys
import os
import socket

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_visual_test():
    print("========================================")
    print("📺 MESAFLOW VISUAL TEST RUNNER (HEADED)")
    print("========================================")

    if not check_port(8000):
        print("❌ ERRO: Backend offline na porta 8000.")
        sys.exit(1)

    print("🚀 Iniciando Playwright em modo visível...")
    print("👉 Observe a janela do navegador que será aberta.")
    
    # Comando para rodar o teste específico com interface e slow-mo para acompanhamento
    cmd = "npx playwright test tests/delivery_e2e.spec.ts --headed --project=chromium"
    
    try:
        subprocess.run(cmd, shell=True, cwd="frontend")
    except Exception as e:
        print(f"💥 Erro ao iniciar teste visual: {e}")

if __name__ == "__main__":
    run_visual_test()

