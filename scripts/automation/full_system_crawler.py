import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# ==============================================================================
# 🕷️ FULL SYSTEM CRAWLER (Dynamic QA)
# ==============================================================================
# Navega por todas as rotas mapeadas, realiza login e verifica a presença
# e visibilidade de elementos interativos em tempo de execução.
# ==============================================================================

BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
REPORT_DIR = Path("testesvisuais/crawler_report")
AUTH_STATE = "auth_state.json"

async def run_crawler():
    print("🕷️  Iniciando Crawler Sistêmico...")
    
    if not os.path.exists(ROUTES_FILE):
        print("❌ Arquivo de rotas não encontrado. Execute map_routes.py primeiro.")
        return

    with open(ROUTES_FILE, "r") as f:
        routes = json.load(f)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None)
        
        # Garante login se não tiver estado salvo
        if not os.path.exists(AUTH_STATE):
            print("🔑 Realizando Login Inicial...")
            page = await context.new_page()
            try:
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard", timeout=10000)
                await context.storage_state(path=AUTH_STATE)
                print("   ✅ Login realizado e estado salvo.")
            except Exception as e:
                print(f"   ❌ Falha no login: {e}")
                await browser.close()
                return

        results = []
        
        for route in routes:
            url = f"{BASE_URL}{route['test_url']}"
            print(f"🔭 Visitando: {url}")
            
            page = await context.new_page()
            try:
                response = await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                # CORREÇÃO: Removidos parênteses. response.status é uma propriedade (int) nesta versão.
                status = response.status if response else 0
                
                # Coleta métricas
                buttons = await page.locator("button:visible").count()
                links = await page.locator("a:visible").count()
                inputs = await page.locator("input:visible").count()
                
                # Screenshot
                safe_name = route['route_pattern'].replace("/", "_").strip("_") or "home"
                screenshot_path = REPORT_DIR / f"{safe_name}.png"
                await page.screenshot(path=screenshot_path)
                
                result = {
                    "route": route['route_pattern'],
                    "url": url,
                    "status": status,
                    "elements": {
                        "buttons": buttons,
                        "links": links,
                        "inputs": inputs
                    },
                    "screenshot": str(screenshot_path)
                }
                results.append(result)
                print(f"   ✅ Status: {status} | Btn: {buttons} | Link: {links} | Inp: {inputs}")
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                results.append({
                    "route": route['route_pattern'],
                    "url": url,
                    "status": "ERROR",
                    "error": str(e)
                })
            finally:
                await page.close()

        # Gerar Relatório HTML Simples
        html_report = "<h1>Relatório de Crawler Sistêmico</h1><table border='1'><tr><th>Rota</th><th>Status</th><th>Botões</th><th>Links</th><th>Inputs</th><th>Screenshot</th></tr>"
        for r in results:
            if "error" in r:
                html_report += f"<tr><td>{r['route']}</td><td style='color:red'>ERROR</td><td colspan='4'>{r['error']}</td></tr>"
            else:
                html_report += f"<tr><td>{r['route']}</td><td>{r['status']}</td><td>{r['elements']['buttons']}</td><td>{r['elements']['links']}</td><td>{r['elements']['inputs']}</td><td><a href='{Path(r['screenshot']).name}'>Ver</a></td></tr>"
        html_report += "</table>"
        
        (REPORT_DIR / "index.html").write_text(html_report, encoding="utf-8")
        print(f"\n📄 Relatório gerado em: {REPORT_DIR}/index.html")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_crawler())

