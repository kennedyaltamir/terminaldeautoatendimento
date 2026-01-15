# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 16:45:00
import subprocess
import socket
import sys
import os
import time
from datetime import datetime

# ==============================================================================
# 🏁 MESAFLOW TEST ORCHESTRATOR (L6)
# ==============================================================================
# Este script verifica o ambiente, executa a suíte completa e gera um relatório.
# ==============================================================================

REPORT_PATH = "governance/evidence/FULL_TEST_SUITE_REPORT.md"

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_command(name, cmd, cwd=None):
    print(f"🚀 Executando: {name}...")
    start = time.time()
    try:
        # shell=True necessário no Windows
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
        return {
            "name": name,
            "status": "💥 ERROR",
            "duration": "0s",
            "output": "",
            "error": str(e)
        }

def main():
    print("====================================================")
    print("🛡️  MESAFLOW OMNI-TESTER v1.0")
    print("====================================================")

    # 1. INSPECTION: Verificação de Prontidão
    backend_up = check_port(8000)
    frontend_up = check_port(3000)

    if not backend_up:
        print("❌ BLOQUEIO: Backend (8000) offline. Inicie o 'python run.py'.")
        sys.exit(1)
    
    results = []

    # 2. ACTION: Execução da Suíte
    # A. Backend (Pytest)
    results.append(run_command("Backend (Lógica/Segurança)", "pytest tests/backend/test_logistics_core.py -v"))

    # B. Realtime & Load (k6) - Verifica se k6 existe
    k6_check = subprocess.run("k6 version", shell=True, capture_output=True)
    if k6_check.returncode == 0:
        results.append(run_command("Realtime (WebSocket v2)", "k6 run tests/realtime/ws_v2_load.js"))
        results.append(run_command("Escala (1000 Drivers)", "k6 run tests/load/scale_1k_drivers.js"))
    else:
        print("⚠️  AVISO: k6 não instalado. Pulando testes de carga/realtime.")
        results.append({"name": "Carga/Realtime", "status": "⏭️ SKIPPED", "duration": "0s", "output": "k6 missing", "error": ""})

    # C. Frontend (Playwright) - Executa a partir da pasta frontend para achar node_modules
    results.append(run_command("Frontend (Fluxo UI)", "npx playwright test ../tests/frontend/logistics_ui.spec.ts", cwd="frontend"))

    # 3. REPORT: Geração de Evidência
    print("\n📝 Gerando relatório final...")
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"# 🛡️ Relatório de Execução de Testes L6\n")
        f.write(f"**Data:** {datetime.now().isoformat()}\n\n")
        f.write("## 📊 Sumário\n")
        f.write("| Teste | Status | Duração |\n")
        f.write("| :--- | :---: | :--- |\n")
        for r in results:
            f.write(f"| {r['name']} | {r['status']} | {r['duration']} |\n")
        
        f.write("\n## 🚩 Detalhes de Falhas\n")
        for r in results:
            if "FAIL" in r["status"] or "ERROR" in r["status"]:
                f.write(f"### ❌ {r['name']}\n")
                f.write("#### STDERR\n```text\n" + r["error"] + "\n```\n")
                f.write("#### STDOUT\n```text\n" + r["output"] + "\n```\n")

    print(f"✅ Suíte finalizada. Relatório em: {REPORT_PATH}")

if __name__ == "__main__":
    main()
