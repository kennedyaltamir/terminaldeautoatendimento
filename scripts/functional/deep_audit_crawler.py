import time
import json
import os
import http.client
import requests
from playwright.sync_api import sync_playwright, Page

# ============================================================
# CONFIGURAÇÃO
# ============================================================
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
REPORT_FILE = "docs/DEEP_AUDIT_REPORT.md"
SCREENSHOT_DIR = "docs/audit_screenshots"

ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

BLACKLIST_TEXT = ["Sair", "Logout", "Excluir", "Deletar", "Delete", "Remover", "Limpar Banco"]

ROUTES = [
    f"/{SLUG}/menu",
    f"/{SLUG}/kiosk",
    f"/admin/{SLUG}/dashboard",
    f"/admin/{SLUG}/menu",
    f"/admin/{SLUG}/tables",
    f"/admin/{SLUG}/inventory",
    f"/admin/{SLUG}/marketing",
    f"/admin/{SLUG}/team",
    f"/admin/{SLUG}/history",
    f"/admin/{SLUG}/settings",
    f"/admin/{SLUG}/kitchen",
    f"/admin/{SLUG}/waiter",
    f"/admin/{SLUG}/counter",
    f"/admin/{SLUG}/delivery",
]

class MesaFlowAuditor:
    def __init__(self):
        self.results = {}
        self.token = None

    def is_server_running(self):
        try:
            conn = http.client.HTTPConnection("localhost", 3000, timeout=2)
            conn.request("HEAD", "/")
            return conn.getresponse().status < 500
        except:
            return False

    def get_real_token(self):
        try:
            res = requests.post(f"{API_URL}/auth/token", data={
                "username": ADMIN_EMAIL,
                "password": ADMIN_PASS
            }, timeout=5)
            if res.status_code == 200:
                self.token = res.json()["access_token"]
                return True
            return False
        except:
            return False

    def log_error(self, route, error_type, message, page: Page = None):
        # Ignora ruídos de RSC e extensões
        if any(x in message for x in ["favicon", "chrome-extension", "RSC payload"]):
            return

        err = f"[{error_type}] {message}"
        if route not in self.results:
            self.results[route] = []
        
        if err not in self.results[route]:
            self.results[route].append(err)
            print(f"  ❌ {err}")
            if page:
                safe_name = route.replace("/", "_").strip("_")
                page.screenshot(path=f"{SCREENSHOT_DIR}/{safe_name}_error.png")

    def audit_route(self, page: Page, route: str):
        print(f"🔍 Auditando: {route}")
        url = f"{BASE_URL}{route}"
        
        page.on("pageerror", lambda exc: self.log_error(route, "CRASH", exc.message, page))
        page.on("console", lambda msg: self.log_error(route, "CONSOLE", msg.text, page) if msg.type == "error" else None)

        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Detecta erro de build/sintaxe que gera 500 no Next.js
            if response and response.status == 500:
                self.log_error(route, "BUILD_ERROR", "A página falhou ao compilar (500)")
                return

            page.wait_for_timeout(2000)

            elements = page.query_selector_all("button, a, [role='button']")
            for el in elements[:10]:
                try:
                    if not el.is_visible(): continue
                    text = el.inner_text().strip()
                    if any(b.lower() in text.lower() for b in BLACKLIST_TEXT): continue
                    el.click(timeout=1000)
                    page.wait_for_timeout(300)
                except:
                    continue 

        except Exception as e:
            self.log_error(route, "NAVIGATION_FAIL", str(e))

    def generate_report(self):
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("# 🛡️ Relatório de Auditoria Profunda MesaFlow\n\n")
            f.write(f"**Data:** {time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            total_errors = sum(len(v) for v in self.results.values())
            if total_errors == 0:
                f.write("## ✅ Sistema Íntegro!\n")
            else:
                f.write(f"## ⚠️ {total_errors} Inconsistências Detectadas\n\n")
                for route, errs in self.results.items():
                    f.write(f"### `{route}`\n")
                    for e in errs: f.write(f"- {e}\n")
                    f.write("\n")
        print(f"\n✨ Auditoria finalizada. Relatório: {REPORT_FILE}")

def run_audit():
    auditor = MesaFlowAuditor()
    if not auditor.is_server_running() or not auditor.get_real_token():
        print("❌ Erro: Servidor offline ou falha na autenticação.")
        return

    if not os.path.exists(SCREENSHOT_DIR): os.makedirs(SCREENSHOT_DIR)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        context.add_init_script(f"window.localStorage.setItem('mesaflow_access_token', '{auditor.token}');")
        context.add_init_script("window.localStorage.setItem('mesaflow_user_role', 'owner');")
        context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")

        page = context.new_page()
        for route in ROUTES:
            auditor.audit_route(page, route)
            print("-" * 30)
        auditor.generate_report()
        browser.close()

if __name__ == "__main__":
    run_audit()
