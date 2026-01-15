import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# ==============================================================================
# 🕵️ COMPREHENSIVE SYSTEM AUDIT v2.0 (Deep Crawler)
# ==============================================================================
# Objetivo: Navegar por TODAS as 38 páginas do frontend, identificar elementos
# interativos, testar integridade visual e funcional (Smoke Test) e reportar
# anomalias.
# ==============================================================================

BASE_URL = "http://localhost:3000"
REPORT_PATH = Path("governance/evidence/REPORT_FULL_SYSTEM_AUDIT.md")
SCREENSHOT_DIR = Path("testesvisuais/audit")
AUTH_STATE = "auth_state.json"

# Configuração de Parâmetros Dinâmicos
TEST_PARAMS = {
    "[slug]": "hamburgueria-ze",
    "[tableId]": "1"
}

# Lista de Rotas (Extraída do list_frontend_pages.py)
ROUTES = [
    "/",
    "/[slug]/kiosk",
    "/[slug]/menu",
    "/[slug]/monitor",
    "/admin/[slug]/audit",
    "/admin/[slug]/audit/financial",
    "/admin/[slug]/counter",
    "/admin/[slug]/dashboard",
    "/admin/[slug]/dashboard/history",
    "/admin/[slug]/delivery",
    "/admin/[slug]/driver",
    "/admin/[slug]/expeditor",
    "/admin/[slug]/franchise",
    "/admin/[slug]/history",
    "/admin/[slug]/inventory",
    "/admin/[slug]/kitchen",
    "/admin/[slug]/marketing",
    "/admin/[slug]/menu",
    "/admin/[slug]/profile",
    "/admin/[slug]/settings",
    "/admin/[slug]/settings/billing",
    "/admin/[slug]/settings/features",
    "/admin/[slug]/tables",
    "/admin/[slug]/team",
    "/admin/[slug]/waiter",
    "/admin/[slug]/waiter/orders",
    "/admin/[slug]/waiter/pos/[tableId]",
    "/admin/[slug]/waiter/pos/quick",
    "/admin/forgot-password",
    "/admin/login",
    "/admin/payment/callback",
    "/admin/register",
    "/admin/reset-password",
    "/admin/support",
    "/offline",
    "/trust",
    "/trust/security",
    "/trust/status"
]

class SystemAuditor:
    def __init__(self):
        self.results = []
        self.total_elements = 0
        self.total_issues = 0
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def resolve_url(self, route):
        url = route
        for key, value in TEST_PARAMS.items():
            url = url.replace(key, value)
        return url

    async def ensure_login(self, browser):
        if not os.path.exists(AUTH_STATE):
            print("🔑 Realizando Login Administrativo para Auditoria...")
            page = await browser.new_page()
            try:
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard", timeout=15000)
                await page.context.storage_state(path=AUTH_STATE)
                print("   ✅ Login realizado. Estado salvo.")
            except Exception as e:
                print(f"   ❌ Falha crítica no login: {e}")
                return False
            finally:
                await page.close()
        return True

    async def audit_page(self, context, route):
        url = f"{BASE_URL}{self.resolve_url(route)}"
        print(f"🔭 Auditando: {route} -> {url}")
        
        page = await context.new_page()
        errors = []
        
        # Captura de Erros
        page.on("console", lambda msg: errors.append(f"CONSOLE: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"CRASH: {exc}"))
        page.on("response", lambda res: errors.append(f"HTTP {res.status}: {res.url}") if res.status >= 400 else None)

        try:
            response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            status = response.status if response else 0
            
            # Aguarda hidratação básica
            await asyncio.sleep(1)

            # Inventário de Elementos
            buttons = await page.locator("button:visible").all()
            links = await page.locator("a:visible").all()
            inputs = await page.locator("input:visible").all()
            
            element_count = len(buttons) + len(links) + len(inputs)
            self.total_elements += element_count

            # Teste de Interatividade (Smoke Test)
            # Verifica se botões críticos estão habilitados
            disabled_buttons = 0
            for btn in buttons:
                if await btn.is_disabled():
                    disabled_buttons += 1
            
            # Screenshot
            # CORREÇÃO: Nome de arquivo seguro para Windows
            safe_name = route.replace("/", "_").replace("[", "").replace("]", "").strip("_")
            if not safe_name: safe_name = "home" # Caso seja a raiz
            screenshot_path = SCREENSHOT_DIR / f"{safe_name}.png"
            await page.screenshot(path=screenshot_path)

            result = {
                "route": route,
                "url": url,
                "status": status,
                "elements": {
                    "buttons": len(buttons),
                    "links": len(links),
                    "inputs": len(inputs),
                    "disabled_buttons": disabled_buttons
                },
                "errors": errors,
                "screenshot": str(screenshot_path)
            }
            
            status_icon = "✅" if status == 200 and not errors else "⚠️" if errors else "❌"
            print(f"   {status_icon} Status: {status} | Elementos: {element_count} | Erros: {len(errors)}")
            
            self.results.append(result)

        except Exception as e:
            print(f"   ❌ Erro de execução: {e}")
            self.results.append({
                "route": route,
                "url": url,
                "status": "ERROR",
                "error": str(e),
                "elements": {"buttons": 0, "links": 0, "inputs": 0, "disabled_buttons": 0},
                "errors": [str(e)]
            })
        finally:
            await page.close()

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            if not await self.ensure_login(browser):
                return

            context = await browser.new_context(storage_state=AUTH_STATE)
            
            for route in ROUTES:
                await self.audit_page(context, route)
            
            await browser.close()
            self.generate_report()

    def generate_report(self):
        print("\n📝 Gerando Relatório de Auditoria Sistêmica...")
        
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("# 🕵️ Relatório de Auditoria Sistêmica (Full Coverage)\n")
            f.write(f"**Data:** {datetime.now().isoformat()}\n")
            f.write(f"**Páginas Auditadas:** {len(self.results)}\n")
            f.write(f"**Total de Elementos Interativos:** {self.total_elements}\n\n")
            
            f.write("## 1. Matriz de Status\n")
            f.write("| Rota | Status | Botões | Links | Inputs | Erros |\n")
            f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
            
            for r in self.results:
                status_icon = "✅" if r["status"] == 200 and not r.get("errors") else "⚠️" if r.get("errors") else "❌"
                err_count = len(r.get("errors", []))
                f.write(f"| `{r['route']}` | {status_icon} {r['status']} | {r['elements']['buttons']} | {r['elements']['links']} | {r['elements']['inputs']} | {err_count} |\n")
            
            f.write("\n## 2. Detalhamento de Anomalias\n")
            has_errors = False
            for r in self.results:
                if r.get("errors"):
                    has_errors = True
                    f.write(f"### 🚩 {r['route']}\n")
                    f.write("```text\n")
                    for err in r["errors"]:
                        f.write(f"- {err}\n")
                    f.write("```\n")
            
            if not has_errors:
                f.write("✅ Nenhuma anomalia crítica detectada nos logs de console ou rede.\n")

        print(f"✅ Relatório salvo em: {REPORT_PATH}")

if __name__ == "__main__":
    auditor = SystemAuditor()
    asyncio.run(auditor.run())

