import os
import sys
import io
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🛡️ THE GREAT FILTER v1.1 (Robust Edition)
# ==============================================================================
# Objetivo: Testar em massa, filtrar e protocolar scripts funcionais.
# Changelog: Adicionada lista de ignorados para scripts interativos/daemons.
# ==============================================================================

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurações
SOURCE_DIR = Path("scripts")
TARGET_DIR = Path("canonic")
LOG_FILE = TARGET_DIR / "execution_report.md"
REGISTRY_FILE = TARGET_DIR / "registry.xml"
TIMEOUT_SECONDS = 10  # Reduzido para falhar mais rápido em scripts travados

# 🚫 BLACKLIST: Scripts que sabemos que travam, abrem UI ou são daemons
IGNORE_LIST = [
    "the_great_filter.py",
    "run.py", 
    "setup_redis.py", 
    "launch.bat",
    "dev.bat",
    "atualizar.py",
    "gerartxt.py",
    "comprehensive_behavior_test.py", # Travou na última execução
    "delivery_realtime_simulation.py", # Depende de Server
    "run_human_qa.py", # Abre navegador
    "optimus_v9_1_neuro_evolution.py", # Loop infinito
    "full_system_crawler.py", # Demorado
    "driver_pickup_simulation.py", # Depende de Server
    "pompeu_delivery_simulation.py", # Depende de Server
    "dual_screen_delivery_sim.py", # Depende de Server
    "enterprise_delivery_l8.py", # Depende de Server
    "run_delivery_e2e.bat",
    "run_kiosk_tests.py"
]

def setup_canonic_env():
    """Prepara o ambiente limpo em canonic/"""
    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True)
    
    # Criar estrutura básica do Registry se não existir
    if not REGISTRY_FILE.exists():
        root = ET.Element("Registry", version="1.0", authority="The Great Filter")
        meta = ET.SubElement(root, "Meta")
        ET.SubElement(meta, "GeneratedAt").text = datetime.now().isoformat()
        ET.SubElement(root, "Scripts")
        tree = ET.ElementTree(root)
        tree.write(REGISTRY_FILE, encoding="utf-8", xml_declaration=True)

def register_success(script_path, duration):
    """Adiciona o script aprovado ao registry.xml"""
    try:
        tree = ET.parse(REGISTRY_FILE)
        root = tree.getroot()
        scripts_node = root.find("Scripts")
        
        # Remove entrada anterior se existir
        script_name = script_path.name
        for existing in scripts_node.findall("Script"):
            if existing.get("name") == script_name:
                scripts_node.remove(existing)
                
        # Adiciona nova entrada
        new_entry = ET.SubElement(scripts_node, "Script")
        script_hash = abs(hash(script_name)) % 10000
        new_entry.set("id", f"CANON-{script_hash:04d}")
        new_entry.set("name", script_name)
        new_entry.set("original_path", str(script_path))
        new_entry.set("status", "SUCCESS")
        new_entry.set("certified_at", datetime.now().isoformat())
        new_entry.set("execution_time", f"{duration:.2f}s")
        
        tree.write(REGISTRY_FILE, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        print(f"⚠️ Erro ao registrar XML: {e}")

def run_filter():
    print(f"🚀 Iniciando THE GREAT FILTER em: {SOURCE_DIR}")
    setup_canonic_env()
    
    results = {"PASS": [], "FAIL": [], "TIMEOUT": []}
    
    # Coletar todos os scripts .py
    all_scripts = list(SOURCE_DIR.rglob("*.py"))
    total = len(all_scripts)
    
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write(f"# 🛡️ Relatório de Execução - The Great Filter\n")
        log.write(f"**Data:** {datetime.now()}\n\n")
        log.write("| Script | Status | Tempo | Erro |\n")
        log.write("| :--- | :---: | :---: | :--- |\n")

        for idx, script in enumerate(all_scripts):
            if script.name in IGNORE_LIST or "venv" in str(script):
                continue
                
            print(f"[{idx+1}/{total}] Testando: {script.name}...", end=" ", flush=True)
            
            start_time = time.time()
            try:
                env = os.environ.copy()
                env["PYTHONPATH"] = os.getcwd()
                env["PYTHONIOENCODING"] = "utf-8"
                
                # Execução isolada
                result = subprocess.run(
                    [sys.executable, str(script)],
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_SECONDS,
                    env=env,
                    encoding='utf-8',
                    errors='replace'
                )
                
                duration = time.time() - start_time
                
                if result.returncode == 0:
                    print(f"✅ PASS ({duration:.2f}s)")
                    results["PASS"].append(script.name)
                    
                    dest_file = TARGET_DIR / script.name
                    shutil.copy2(script, dest_file)
                    register_success(script, duration)
                    
                    log.write(f"| `{script.name}` | 🟢 PASS | {duration:.2f}s | - |\n")
                else:
                    print(f"❌ FAIL")
                    results["FAIL"].append(script.name)
                    # Fix SyntaxWarning: use raw string or double escape
                    error_snippet = "\n".join(result.stderr.splitlines()[-3:]).replace("|", "\\|") if result.stderr else "Exit Code != 0"
                    log.write(f"| `{script.name}` | 🔴 FAIL | {duration:.2f}s | {error_snippet} |\n")

            except subprocess.TimeoutExpired:
                print(f"⏱️ TIMEOUT")
                results["TIMEOUT"].append(script.name)
                log.write(f"| `{script.name}` | 🟡 TIMEOUT | >{TIMEOUT_SECONDS}s | Execução interrompida |\n")
            except Exception as e:
                print(f"⚠️ ERROR: {e}")
                log.write(f"| `{script.name}` | 💥 CRASH | - | {str(e)} |\n")

    print("\n" + "="*40)
    print("📊 RESUMO DO FILTRO")
    print("="*40)
    print(f"✅ Aprovados: {len(results['PASS'])}")
    print(f"❌ Falharam:  {len(results['FAIL'])}")
    print(f"⏱️ Timeouts:  {len(results['TIMEOUT'])}")
    print(f"\n📁 Scripts aprovados copiados para: {TARGET_DIR}")
    print(f"📜 Protocolo gerado em: {REGISTRY_FILE}")

if __name__ == "__main__":
    run_filter()

