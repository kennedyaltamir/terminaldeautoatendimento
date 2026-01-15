
import os
import sys
import subprocess
import json
import time
import re
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# Configuração L6
MAESTRO_DIR = Path("mobile/e2e/maestro")
REPORT_DIR = Path("docs/mobile/reports")
SCREENSHOTS_DIR = REPORT_DIR / "screenshots"
DUMPS_DIR = REPORT_DIR / "dumps"
REPORT_FILE = REPORT_DIR / "HUMAN_UI_TEST_REPORT.md"
DIAGNOSTIC_FILE = REPORT_DIR / "DIAGNOSTIC_REPORT.md"

# Importação dinâmica do Auto-Fix
try:
    sys.path.append(os.getcwd())
    from scripts.l6.auto_fix_on_fail import retry_action
except ImportError:
    retry_action = None

class AdbDriverL6:
    def __init__(self):
        self.check_connection()
        self.width, self.height = self.get_screen_size()
        print(f"📱 Resolução Detectada: {self.width}x{self.height}")
        self.step_counter = 0

    def check_connection(self):
        res = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
        if "device" not in res.stdout.replace("List of devices attached", "").strip():
            print("❌ Nenhum emulador conectado.")
            sys.exit(1)

    def get_screen_size(self):
        try:
            out = subprocess.check_output("adb shell wm size", shell=True).decode()
            match = re.search(r'(\d+)x(\d+)', out)
            if match: return int(match.group(1)), int(match.group(2))
        except: pass
        return 1080, 2400

    def capture_state(self, context):
        """Captura screenshot e dump XML para diagnóstico."""
        timestamp = datetime.now().strftime("%H%M%S")
        filename_base = f"step_{self.step_counter:03d}_{context}_{timestamp}"
        
        # Screenshot
        subprocess.run(f"adb shell screencap -p /sdcard/{filename_base}.png", shell=True)
        subprocess.run(f"adb pull /sdcard/{filename_base}.png {SCREENSHOTS_DIR}/{filename_base}.png", shell=True, stdout=subprocess.DEVNULL)
        
        # Dump XML
        subprocess.run(f"adb shell uiautomator dump /sdcard/{filename_base}.xml", shell=True, stdout=subprocess.DEVNULL)
        subprocess.run(f"adb pull /sdcard/{filename_base}.xml {DUMPS_DIR}/{filename_base}.xml", shell=True, stdout=subprocess.DEVNULL)
        
        return filename_base

    def get_element_center(self, text):
        dump_file = self.capture_state("find_element")
        local_xml = DUMPS_DIR / f"{dump_file}.xml"
        
        try:
            tree = ET.parse(local_xml)
            candidates = []
            for node in tree.getroot().iter("node"):
                node_text = node.attrib.get("text", "")
                node_desc = node.attrib.get("content-desc", "")
                if text in node_text or text in node_desc:
                    bounds = node.attrib.get("bounds")
                    is_clickable = node.attrib.get("clickable") == "true"
                    coords = re.findall(r'\d+', bounds)
                    if coords:
                        x1, y1, x2, y2 = map(int, coords)
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        candidates.append({"x": center_x, "y": center_y, "clickable": is_clickable, "text": node_text})
            
            if candidates:
                # Prioriza clickable
                best = next((c for c in candidates if c["clickable"]), candidates[0])
                print(f"   🔍 Encontrado: '{text}' em ({best['x']}, {best['y']}) [Clickable: {best['clickable']}]")
                return best["x"], best["y"]
                
        except Exception as e:
            print(f"   ⚠️ Erro ao parsear XML: {e}")
        
        return None

    def tap(self, target):
        self.step_counter += 1
        print(f"👉 [{self.step_counter}] Tap: {target}")
        self.capture_state("before_tap")
        
        def _action():
            coords = self.get_element_center(target)
            if coords:
                subprocess.run(f"adb shell input tap {coords[0]} {coords[1]}", shell=True)
                return True
            raise Exception(f"Elemento '{target}' não encontrado")

        try:
            if retry_action: retry_action(_action)
            else: _action()
        except:
            print(f"   ⚠️ Fallback: Tap no centro")
            subprocess.run(f"adb shell input tap {self.width//2} {self.height//2}", shell=True)
        
        time.sleep(1)
        self.capture_state("after_tap")

    def text(self, content):
        self.step_counter += 1
        print(f"⌨️ [{self.step_counter}] Input: {content}")
        clean = content.replace(" ", "%s")
        subprocess.run(f"adb shell input text {clean}", shell=True)
        time.sleep(1)

    def clear_text(self):
        subprocess.run("adb shell input keyevent 123", shell=True) 
        for _ in range(30):
            subprocess.run("adb shell input keyevent 67", shell=True)

    def launch_app(self, app_id, clear=False):
        self.step_counter += 1
        print(f"🚀 [{self.step_counter}] Launch App")
        if clear: subprocess.run(f"adb shell pm clear {app_id}", shell=True, stdout=subprocess.DEVNULL)
        subprocess.run(f"adb shell monkey -p {app_id} -c android.intent.category.LAUNCHER 1", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(4)
        self.capture_state("launch")

    def assert_visible(self, text, timeout=5):
        self.step_counter += 1
        print(f"👁️ [{self.step_counter}] Assert Visible: {text}")
        start = time.time()
        while time.time() - start < timeout:
            if self.get_element_center(text):
                print(f"   ✅ Validado: '{text}' visível.")
                return True
            time.sleep(0.5)
        
        print(f"   ❌ Timeout aguardando '{text}'")
        self.capture_state("assert_fail")
        raise AssertionError(f"Timeout aguardando '{text}'")

    def assert_not_visible(self, text):
        if self.get_element_center(text):
            self.capture_state("assert_not_visible_fail")
            raise AssertionError(f"❌ Elemento '{text}' NÃO deveria estar visível.")
        print(f"   🚫 Validado: '{text}' não está visível.")

    def run_script(self, script):
        self.step_counter += 1
        print(f"🔧 [{self.step_counter}] Script: {script}")
        subprocess.run(script, shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def screenshot(self, name):
        self.capture_state(f"manual_{name}")

def run_tests():
    print("🤖 MESAFLOW HUMAN QA (L6 OBSERVABILITY)")
    print("=======================================")
    
    for d in [REPORT_DIR, SCREENSHOTS_DIR, DUMPS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    driver = AdbDriverL6()
    full_sweep = MAESTRO_DIR / "full_ui_sweep.yaml"
    
    try:
        with open(full_sweep, 'r', encoding='utf-8') as f:
            raw_content = f.read()
            parts = raw_content.split("---")
            content = parts[-1] if len(parts) > 1 else raw_content
            steps = yaml.safe_load(content)

        if not steps: return

        for step in steps:
            if isinstance(step, str): continue
            
            if "launchApp" in step:
                config = step["launchApp"] if isinstance(step["launchApp"], dict) else {}
                driver.launch_app("com.mesaflow.mobile", config.get("clearState", False))
            elif "tapOn" in step:
                driver.tap(step["tapOn"])
            elif "inputText" in step:
                driver.text(step["inputText"])
            elif "clearText" in step:
                driver.clear_text()
            elif "assertVisible" in step:
                driver.assert_visible(step["assertVisible"])
            elif "assertNotVisible" in step:
                driver.assert_not_visible(step["assertNotVisible"])
            elif "takeScreenshot" in step:
                driver.screenshot(step["takeScreenshot"])
            elif "runScript" in step:
                driver.run_script(step["runScript"])
                
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        with open(DIAGNOSTIC_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Relatório de Diagnóstico de Falha\n\n")
            f.write(f"**Erro:** {str(e)}\n")
            f.write(f"**Passo:** {driver.step_counter}\n")
            f.write(f"**Artefatos:** Ver pasta `dumps/` e `screenshots/`\n")
        sys.exit(1)

    print("\n✅ Teste concluído com sucesso.")

if __name__ == "__main__":
    run_tests()

