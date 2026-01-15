# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 17:10:00
import subprocess
import socket
import sys
import os
import time
from datetime import datetime

# ==============================================================================
# 🏁 MESAFLOW TEST ORCHESTRATOR v1.1 (Path-Safe Windows)
# ==============================================================================

REPORT_PATH = "governance/evidence/FULL_TEST_SUITE_REPORT.md"
ROOT_DIR = os.getcwd()

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_command(name, cmd, cwd=None):
    print(f"🚀 Executando: {name}...")
    start = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, encoding='utf-8', errors='replace')
        duration = time.time() - start
        status = "✅ PASS" if result.returncode == 0 else "❌ FAIL"
        return {
            "name": name,
            "status": status,
            "duration": f"{duration:.2f}s",
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return { "name": name, "status": "💥 ERROR", "duration": "0s", "output": "", "error": str(e) }

def main():
    print("====================================================")
    print("🛡️  MESAFLOW OMNI-TESTER v1.1")
    print("====================================================")

    if not check_port(8000):
        print("❌ BLOQUEIO: Backend offline na porta 8000.")
        sys.exit(1)
    
    results = []

    # A. Backend (Pytest)
    # Define PYTHONPATH para garantir que o pytest encontre o app na raiz
    os.environ["PYTHONPATH"] = ROOT_DIR
    results.append(run_command("Backend (Lógica/Segurança)", "pytest tests/backend/test_logistics_core.py -v"))

    # B. Carga/Realtime (k6)
    k6_check = subprocess.run("k6 version", shell=True, capture_output=True)
    if k6_check.returncode == 0:
        results.append(run_command("Realtime (WebSocket v2)", "k6 run tests/realtime/ws_v2_load.js"))
        results.append(run_command("Escala (1000 Drivers)", "k6 run tests/load/scale_1k_drivers.js"))
    else:
        results.append({"name": "Carga/Realtime", "status": "⏭️ SKIPPED", "duration": "0s", "output": "k6 not installed", "error": ""})

    # C. Frontend (Playwright)
    # Fix: Chama o playwright de dentro da pasta frontend, mas aponta para o teste na pasta de testes global
    # Usamos o caminho absoluto para evitar erros de resolução de diretório pai no Windows
    test_file = os.path.abspath("tests/frontend/logistics_ui.spec.ts")
    results.append(run_command("Frontend (Fluxo UI)", f"npx playwright test \"{test_file}\"", cwd="frontend"))

    # 3. REPORT
    print("\n📝 Consolidando evidências...")
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"# 🛡️ Relatório de Execução de Testes L6\n")
        f.write(f"**Data:** {datetime.now().isoformat()}\n\n")
        f.write("## 📊 Sumário\n| Teste | Status | Duração |\n| :--- | :---: | :--- |\n")
        for r in results:
            f.write(f"| {r['name']} | {r['status']} | {r['duration']} |\n")
        f.write("\n## 🚩 Detalhes de Falhas\n")
        for r in results:
            if "FAIL" in r["status"] or "ERROR" in r["status"]:
                f.write(f"### ❌ {r['name']}\n#### STDERR\n```text\n{r['error']}\n```\n#### STDOUT\n```text\n{r['output']}\n```\n")

    print(f"✅ Relatório atualizado em: {REPORT_PATH}")

if __name__ == "__main__":
    main()
