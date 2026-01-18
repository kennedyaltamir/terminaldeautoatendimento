import os
import sys
import io
import subprocess
import time
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🏅 CANONIC SUITE RUNNER
# ==============================================================================
# Objetivo: Executar a elite dos scripts (canonic/) e gerar um relatório de saúde.
# ==============================================================================

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CANONIC_DIR = Path("canonic")
REPORT_FILE = CANONIC_DIR / "health_report.md"
TIMEOUT_SECONDS = 20

def run_suite():
    print(f"🚀 Iniciando execução da Suíte Canônica ({CANONIC_DIR})...")
    
    scripts = sorted([f for f in CANONIC_DIR.glob("*.py") if f.name != "run_all_canonic.py"])
    total = len(scripts)
    
    results = []
    
    print(f"ℹ️  Encontrados {total} scripts para validar.\n")

    for idx, script in enumerate(scripts):
        print(f"[{idx+1}/{total}] Executando: {script.name}...", end=" ", flush=True)
        
        start_time = time.time()
        status = "UNKNOWN"
        details = ""
        
        try:
            # Configurar ambiente para garantir imports da raiz
            env = os.environ.copy()
            env["PYTHONPATH"] = os.getcwd()
            env["PYTHONIOENCODING"] = "utf-8"

            proc = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                env=env,
                encoding='utf-8',
                errors='replace'
            )
            
            duration = time.time() - start_time
            
            if proc.returncode == 0:
                print(f"✅ PASS ({duration:.2f}s)")
                status = "✅ PASS"
            else:
                print(f"❌ FAIL")
                status = "❌ FAIL"
                # Pegar as últimas 2 linhas do erro
                details = "\n".join(proc.stderr.strip().splitlines()[-2:])
                
        except subprocess.TimeoutExpired:
            print(f"⏱️ TIMEOUT")
            status = "⚠️ TIMEOUT"
            duration = TIMEOUT_SECONDS
        except Exception as e:
            print(f"💥 CRASH")
            status = "💥 CRASH"
            details = str(e)
            duration = 0

        results.append({
            "name": script.name,
            "status": status,
            "duration": duration,
            "details": details
        })

    # Gerar Relatório
    generate_report(results)

def generate_report(results):
    passed = len([r for r in results if "PASS" in r["status"]])
    failed = len([r for r in results if "FAIL" in r["status"]])
    timeouts = len([r for r in results if "TIMEOUT" in r["status"]])
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🏥 MesaFlow Canonic Health Report\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        f.write("## 📊 Resumo\n")
        f.write(f"- **Total:** {len(results)}\n")
        f.write(f"- **Sucesso:** {passed} ({(passed/len(results))*100:.1f}%)\n")
        f.write(f"- **Falhas:** {failed}\n")
        f.write(f"- **Timeouts:** {timeouts}\n\n")
        
        f.write("## 📝 Detalhes\n")
        f.write("| Script | Status | Tempo | Detalhes |\n")
        f.write("| :--- | :---: | :---: | :--- |\n")
        
        for r in results:
            clean_details = r['details'].replace('\n', ' ').replace('|', '\|')[:100]
            f.write(f"| `{r['name']}` | {r['status']} | {r['duration']:.2f}s | {clean_details} |\n")

    print(f"\n📄 Relatório gerado em: {REPORT_FILE}")

if __name__ == "__main__":
    run_suite()

