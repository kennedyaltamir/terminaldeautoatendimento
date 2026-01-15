# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:05:00
import subprocess
import sys
import os
import time
import socket

def check_port(port):
    """Verifica se uma porta está aberta no localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_step(name, cmd, cwd=None):
    print(f"\n🚀 [STEP] {name}")
    print(f"   Executando: {cmd}")
    try:
        # shell=True é necessário no Windows para resolver comandos npm/python
        res = subprocess.run(cmd, shell=True, cwd=cwd)
        if res.returncode != 0:
            print(f"❌ Falha em {name} (Exit Code: {res.returncode})")
            return False
        print(f"✅ Sucesso em {name}")
        return True
    except Exception as e:
        print(f"💥 Erro ao executar {name}: {e}")
        return False

def main():
    print("========================================")
    print("📦 MESAFLOW DELIVERY TEST SUITE (L6)")
    print("========================================")

    # 0. Pre-flight Check: Backend Connectivity
    print("🔍 Verificando conectividade com o Backend...")
    if not check_port(8000):
        print("\n🚨 BLOQUEIO: O Backend (FastAPI) está OFFLINE na porta 8000.")
        print("👉 Ação Requerida: Abra um novo terminal e execute 'python run.py'.")
        sys.exit(1)
    print("   ✅ Backend detectado na porta 8000.")

    # 1. Seed de Dados (Garante estado limpo e determinístico)
    if not run_step("Seed de Dados (Logística)", "python scripts/maintenance/seed_logistics.py"):
        print("⛔ Abortando suite devido a falha no seed.")
        sys.exit(1)

    # 2. Testes E2E (Playwright)
    print("\n🧪 Iniciando Testes Automatizados (Headless)...")
    
    # Define PYTHONPATH para garantir que o Playwright encontre os módulos se necessário
    os.environ["PYTHONPATH"] = os.getcwd()
    
    test_file = "tests/delivery_e2e.spec.ts"
    if not run_step(f"Teste E2E: {test_file}", f"npx playwright test {test_file}", cwd="frontend"):
        print(f"\n⚠️  O teste {test_file} falhou. Verifique os logs do Playwright.")
        sys.exit(1)

    print("\n🏁 Suite de Entrega finalizada com SUCESSO.")

if __name__ == "__main__":
    main()
