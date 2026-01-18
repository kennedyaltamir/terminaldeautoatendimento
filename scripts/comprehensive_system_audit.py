import asyncio
import json
import os
import re
import sys
import io
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# ==============================================================================
# 🕵️ COMPREHENSIVE SYSTEM AUDIT v4.1 (Bugfix Edition)
# ==============================================================================
# Changelog v4.1:
# - FIX: Adicionada chave 'weight' e 'level' no retorno de audit_kiosk_security
#   para evitar KeyError durante o cálculo de score.
# ==============================================================================

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurações
BASE_URL = "http://localhost:3000"
FRONTEND_ROOT = Path("frontend/src/app")
EVIDENCE_DIR = Path("governance/evidence")
REPORT_MD = EVIDENCE_DIR / "REPORT_FULL_SYSTEM_AUDIT.md"
REPORT_JSON = EVIDENCE_DIR / "SYSTEMIC_AUDIT_REPORT.json"
SCREENSHOT_DIR = EVIDENCE_DIR / "screenshots"
AUTH_STATE = "auth_state.json"

# Parâmetros para Rotas Dinâmicas
TEST_PARAMS = {
    "[slug]": "hamburgueria-ze",
    "[tableId]": "1",
    "[orderId]": "mock-order-id",
    "[id]": "1",
    "[categoryId]": "1",
    "[productId]": "1"
}

class ErrorClassifier:
    @staticmethod
    def classify(msg: str, source: str) -> dict:
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ["hydration", "source map", "third-party cookie", "preload"]):
            return {"level": "LOW", "weight": 1}
        if any(x in msg_lower for x in ["warning", "deprecated", "performance"]):
            return {"level": "MEDIUM", "weight": 5}
        if any(x in msg_lower for x in ["401", "403", "cors", "network error", "failed to fetch"]):
            return {"level": "HIGH", "weight": 20}
        if any(x in msg_lower for x in ["typeerror", "referenceerror", "syntaxerror", "unhandled runtime error", "500 internal"]):
            return {"level": "CRITICAL", "weight": 100}
        return {"level": "MEDIUM", "weight": 5}

class SystemAuditor:
    def __init__(self):
        self.results = []
        self.total_elements = 0
        self.system_score = 100
        self.verdict = "UNKNOWN"
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    def discover_routes(self):
        print(f"🔍 Descobrindo rotas em: {FRONTEND_ROOT}")
        routes = []
        for root, dirs, files in os.walk(FRONTEND_ROOT):
            if "page.tsx" in files:
                rel_path = Path(root).relative_to(FRONTEND_ROOT)
                path_str = str(rel_path).replace("\\", "/")
                parts = [p for p in path_str.split("/") if not (p.startswith("(") and p.endswith(")"))]
                clean_path = "/".join(parts)
                route = "/" if clean_path == "." else "/" + clean_path
                routes.append(route)
        return sorted(list(set(routes)))

    def resolve_url(self, route):
        url = route
        for key, value in TEST_PARAMS.items():
            url = url.replace(key, value)
        return url

    def is_relevant_response(self, res):
        if res.status < 400: return False
        url = res.url.lower()
        if any(url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.svg', '.ico', '.css', '.woff', '.woff2', '.ttf', '.map']):
            return False
        return "/api/" in url or res.request.resource_type == "document"

    async def ensure_login(self, browser):
        if not os.path.exists(AUTH_STATE):
            print("🔑 Realizando Login Administrativo...")
            page = await browser.new_page()
            try:
                await page.goto(f"{BASE_URL}/admin/login")
                if "/dashboard" in page.url:
                    await page.context.storage_state(path=AUTH_STATE)
                    return True
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard", timeout=10000)
                await page.context.storage_state(path=AUTH_STATE)
                print("   ✅ Login realizado.")
            except Exception as e:
                print(f"   ⚠️ Login falhou (continuando como guest): {e}")
                return False
            finally:
                await page.close()
        return True

    async def audit_kiosk_security(self, page, route):
        if "kiosk" not in route and "totem" not in route:
            return []
        security_issues = []
        original_url = page.url
        try:
            await page.goto(f"{BASE_URL}/admin/login", timeout=3000)
            if "/admin/login" in page.url:
                security_issues.append({
                    "type": "SECURITY_BREACH",
                    "severity": "CRITICAL",
                    "message": "Kiosk permitiu navegação para rota administrativa",
                    "level": "CRITICAL", # FIX: Adicionado level
                    "weight": 100        # FIX: Adicionado weight
                })
            await page.goto(original_url)
        except:
            pass
        return security_issues

    async def audit_page(self, context, route):
        url = f"{BASE_URL}{self.resolve_url(route)}"
        print(f"🔭 {route}...", end=" ", flush=True)
        page = await context.new_page()
        issues = []
        
        page.on("console", lambda msg: issues.append({
            "type": "CONSOLE",
            "message": msg.text,
            **ErrorClassifier.classify(msg.text, "CONSOLE")
        }) if msg.type == "error" else None)
        
        page.on("pageerror", lambda exc: issues.append({
            "type": "CRASH",
            "message": str(exc),
            "level": "CRITICAL",
            "weight": 100
        }))
        
        page.on("response", lambda res: issues.append({
            "type": "NETWORK",
            "message": f"{res.status} {res.url}",
            "level": "HIGH" if res.status in [401, 403] else "MEDIUM",
            "weight": 20
        }) if self.is_relevant_response(res) else None)

        try:
            response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            status = response.status if response else 0
            try:
                await page.wait_for_load_state("networkidle", timeout=3000)
            except: pass

            kiosk_issues = await self.audit_kiosk_security(page, route)
            issues.extend(kiosk_issues)

            buttons = await page.locator("button:visible").count()
            links = await page.locator("a:visible").count()
            inputs = await page.locator("input:visible").count()
            
            safe_name = route.replace("/", "_").replace("[", "").replace("]", "").strip("_") or "home"
            screenshot_path = SCREENSHOT_DIR / f"{safe_name}.png"
            await page.screenshot(path=screenshot_path)

            route_penalty = sum(i['weight'] for i in issues)
            route_score = max(0, 100 - route_penalty)
            
            if route_score == 100: icon = "✅"
            elif route_score >= 80: icon = "⚠️"
            else: icon = "❌"
            
            print(f"{icon} Score: {route_score}")

            self.results.append({
                "route": route,
                "url": url,
                "status": status,
                "score": route_score,
                "elements": {"buttons": buttons, "links": links, "inputs": inputs},
                "issues": issues,
                "screenshot": str(screenshot_path)
            })

        except Exception as e:
            print(f"💥 CRASH")
            self.results.append({
                "route": route,
                "url": url,
                "status": "ERR",
                "score": 0,
                "elements": {},
                "issues": [{"type": "EXECUTION_ERROR", "message": str(e), "level": "CRITICAL", "weight": 100}],
                "screenshot": None
            })
        finally:
            await page.close()

    def calculate_verdict(self):
        total_score = sum(r['score'] for r in self.results)
        avg_score = total_score / len(self.results) if self.results else 0
        critical_fails = any(any(i['level'] == 'CRITICAL' for i in r['issues']) for r in self.results)
        if critical_fails: return "SYSTEM_BROKEN"
        elif avg_score < 80: return "SYSTEM_DEGRADED"
        else: return "SYSTEM_OPERATIONAL"

    def generate_reports(self):
        verdict = self.calculate_verdict()
        timestamp = datetime.now().isoformat()
        json_data = {
            "timestamp": timestamp,
            "verdict": verdict,
            "summary": {
                "total_pages": len(self.results),
                "avg_score": sum(r['score'] for r in self.results) / len(self.results) if self.results else 0
            },
            "details": self.results
        }
        with open(REPORT_JSON, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        with open(REPORT_MD, "w", encoding="utf-8") as f:
            f.write(f"# 🕵️ Relatório de Auditoria Sistêmica v4.1\n")
            f.write(f"**Data:** {timestamp}\n")
            f.write(f"**Veredito:** `{verdict}`\n\n")
            f.write("## 1. Matriz de Saúde\n")
            f.write("| Rota | Score | Status | Elementos | Problemas |\n")
            f.write("| :--- | :---: | :---: | :---: | :--- |\n")
            for r in self.results:
                icon = "✅" if r['score'] == 100 else "⚠️" if r['score'] >= 80 else "❌"
                issues_summary = ", ".join([f"{i['level']}: {i['type']}" for i in r['issues']]) or "-"
                elems = sum(r['elements'].values()) if r['elements'] else 0
                f.write(f"| `{r['route']}` | {r['score']} | {icon} {r['status']} | {elems} | {issues_summary} |\n")
            f.write("\n## 2. Detalhamento de Falhas Críticas/Altas\n")
            has_critical = False
            for r in self.results:
                high_issues = [i for i in r['issues'] if i['level'] in ['CRITICAL', 'HIGH']]
                if high_issues:
                    has_critical = True
                    f.write(f"### 🚩 {r['route']} (Score: {r['score']})\n")
                    f.write("```text\n")
                    for i in high_issues:
                        f.write(f"[{i['level']}] {i['type']}: {i['message']}\n")
                    f.write("```\n")
            if not has_critical:
                f.write("✅ Nenhuma falha crítica ou alta detectada.\n")
        print(f"\n📄 Relatórios gerados:\n   JSON: {REPORT_JSON}\n   MD:   {REPORT_MD}\n   Veredito: {verdict}")

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            await self.ensure_login(browser)
            context = await browser.new_context(storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None)
            routes = self.discover_routes()
            for route in routes:
                await self.audit_page(context, route)
            await browser.close()
            self.generate_reports()

if __name__ == "__main__":
    auditor = SystemAuditor()
    asyncio.run(auditor.run())

