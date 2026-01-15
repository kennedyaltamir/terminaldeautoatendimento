
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 09:40:00
import os
import time
import subprocess
import xml.etree.ElementTree as ET
import re
from datetime import datetime
from pathlib import Path

PACKAGE = "com.mesaflow.mobile"
REPORT_DIR = Path("docs/mobile/reports/full_audit")
TIMESTAMP = datetime.now().strftime("%H%M%S")

class L6FullSuiteAuditor:
    def __init__(self):
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        self.results = []

    def shell(self, cmd):
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)

    def log(self, msg, type="INFO"):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{type}] {msg}")

    def get_xml(self):
        self.shell("adb shell uiautomator dump /sdcard/view.xml")
        xml_path = REPORT_DIR / "current.xml"
        self.shell(f"adb pull /sdcard/view.xml {xml_path}")
        return xml_path

    def find_element(self, pattern):
        xml_path = self.get_xml()
        try:
            tree = ET.parse(xml_path)
            for node in tree.iter('node'):
                text = node.attrib.get('text', '')
                cdesc = node.attrib.get('content-desc', '')
                if re.search(pattern, text, re.I) or re.search(pattern, cdesc, re.I):
                    return node.attrib
        except: pass
        return None

    def tap_element(self, pattern, name):
        el = self.find_element(pattern)
        if el:
            b = re.findall(r'\d+', el.get('bounds'))
            x, y = (int(b[0])+int(b[2]))//2, (int(b[1])+int(b[3]))//2
            self.log(f"Clicando em {name} em [{x}, {y}]")
            self.shell(f"adb shell input tap {x} {y}")
            return True
        return False

    def run_test(self, id, title, action_fn, expected):
        self.log(f"--- {id}: {title} ---")
        start = time.time()
        action_fn()
        
        success = False
        for _ in range(10):
            if self.find_element(expected):
                success = True
                break
            time.sleep(1)
            
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({"id": id, "title": title, "status": status, "time": f"{time.time()-start:.2f}s"})
        self.log(f"Resultado: {status}")

    def generate_report(self):
        report_path = REPORT_DIR / f"FULL_L6_REPORT_{TIMESTAMP}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Relatório de Auditoria Completa L6\n\n")
            f.write("| ID | Teste | Status | Tempo |\n|---|---|---|---|\n")
            for r in self.results:
                f.write(f"| {r['id']} | {r['title']} | {r['status']} | {r['time']} |\n")
        print(f"\n✨ Relatório gerado: {report_path}")

if __name__ == "__main__":
    auditor = L6FullSuiteAuditor()
    
    # Reset
    auditor.shell(f"adb shell am force-stop {PACKAGE}")
    auditor.shell(f"adb shell monkey -p {PACKAGE} 1")
    time.sleep(5)

    # 1. Login Flow
    def login():
        auditor.tap_element("E-mail", "Email Field")
        auditor.shell("adb shell input text 'qa@mesaflow.com'")
        auditor.tap_element("Senha", "Pass Field")
        auditor.shell("adb shell input text '123456'")
        auditor.shell("adb shell input keyevent 66")
        auditor.tap_element("Entrar", "Login Button")
    
    auditor.run_test("T01", "Auth Flow", login, "Mapa de Mesas")

    # 2. Waiter Dashboard
    auditor.run_test("T02", "Waiter Dashboard Render", lambda: None, "Mesa 2")

    # 3. Kitchen Switch (Simulado via Logout/Login)
    def to_kitchen():
        auditor.tap_element("Sair", "Logout")
        time.sleep(2)
        auditor.tap_element("E-mail", "Email Field")
        auditor.shell("adb shell input text 'kitchen@mesaflow.com'")
        auditor.tap_element("Senha", "Pass Field")
        auditor.shell("adb shell input text '123456'")
        auditor.tap_element("Entrar", "Login Button")

    auditor.run_test("T03", "Kitchen Dashboard Render", to_kitchen, "Cozinha")

    # 4. Driver Switch
    def to_driver():
        auditor.tap_element("Sair", "Logout")
        time.sleep(2)
        auditor.tap_element("E-mail", "Email Field")
        auditor.shell("adb shell input text 'driver@mesaflow.com'")
        auditor.tap_element("Senha", "Pass Field")
        auditor.shell("adb shell input text '123456'")
        auditor.tap_element("Entrar", "Login Button")

    auditor.run_test("T04", "Driver Dashboard Render", to_driver, "Entregas")

    auditor.generate_report()

