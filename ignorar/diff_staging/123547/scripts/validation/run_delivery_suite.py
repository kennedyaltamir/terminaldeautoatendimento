import subprocess
import sys
import os
import time

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

    # 1. Seed de Dados (Garante estado limpo e determinístico)
    if not run_step("Seed de Dados (Logística)", "python scripts/maintenance/seed_logistics.py"):
        print("⛔ Abortando suite devido a falha no seed.")
        sys.exit(1)

    # 2. Testes E2E (Playwright)
    # Executa os testes headless para validação lógica rápida
    print("\n🧪 Iniciando Testes Automatizados (Headless)...")
    tests = [
        "tests/delivery_e2e.spec.ts",
        # "tests/logistics_ui.spec.ts" # Opcional, focado no happy path primeiro
    ]
    
    failures = 0
    for test_file in tests:
        # Adiciona --headed opcionalmente se quiser ver, mas padrão é headless para CI
        if not run_step(f"Teste E2E: {test_file}", f"npx playwright test {test_file}", cwd="frontend"):
            failures += 1

    if failures > 0:
        print(f"\n⚠️  {failures} testes falharam. Verifique os logs acima.")
        sys.exit(1)
    else:
        print("\n✨ Todos os testes automatizados passaram!")

    print("\n🏁 Suite de Entrega finalizada com SUCESSO.")

if __name__ == "__main__":
    main()
