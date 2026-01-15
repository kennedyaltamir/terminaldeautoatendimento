import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# ==============================================================================
# 🕵️ COMPREHENSIVE BEHAVIOR TESTER (L6)
# ==============================================================================
# Objetivo: Navegar visualmente por todas as telas, interagir com elementos
# seguros, capturar erros de console/rede e gerar um relatório detalhado.
# ==============================================================================

BASE_URL = "http://localhost:3000"
REPORT_PATH = Path("governance/evidence/REPORT_BEHAVIOR_TEST.md")
SCREENSHOT_DIR = Path("testesvisuais/behavior")

# Rotas para visitar e ações específicas (Safe Interaction)
SCENARIOS = [
    {
        "name": "Login Admin",
        "url": "/admin/login",
        "actions": [
            {"type": "fill", "selector": "input[name='email']", "value": "admin@mesaflow.com"},
            {"type": "fill", "selector": "input[name='password']", "value": "123456"},
            {"type": "click", "selector": "button[type='submit']", "wait_nav": True}
        ]
    },
    {
        "name": "Dashboard Principal",
        "url": "/admin/hamburgueria-ze/dashboard",
        "actions": [
            {"type": "hover", "selector": "text=Faturamento"},
            {"type": "hover", "selector": "text=Total Pedidos"}
        ]
    },
    {
        "name": "Cardápio (Admin)",
        "url": "/admin/hamburgueria-ze/menu",
        "actions": [
            {"type": "click", "selector": "button:has-text('Criar Categoria')", "expect_modal": True},
            {"type": "click", "selector": "button:has-text('Cancelar')"} # Fecha modal
        ]
    },
    {
        "name": "Gestão de Mesas",
        "url": "/admin/hamburgueria-ze/tables",
        "actions": [
            {"type": "click", "selector": "button:has-text('Criar a primeira mesa')", "optional": True},
            {"type": "click", "selector": "button:has-text('Cancelar')", "optional": True}
        ]
    },
    {
        "name": "KDS (Cozinha)",
        "url": "/admin/hamburgueria-ze/kitchen",
        "actions": [
            {"type": "click", "selector": "button[title='Tela Cheia']"},
            {"type": "click", "selector": "button[title='Tela Cheia']"} # Toggle back
        ]
    },
    {
        "name": "Menu Público (Cliente)",
        "url": "/hamburgueria-ze/menu",
        "actions": [
            {"type": "click", "selector": "text=X-Bacon", "expect_modal": True},
            {"type": "click", "selector": "button:has-text('Adicionar ao Carrinho')"},
            {"type": "click", "selector": "button:has-text('Ver Carrinho')"}
        ]
    }
]

class BehaviorTester:
    def __init__(self):
        self.errors = []
        self.logs = []
        self.results = []
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        self.logs.append(f"[{timestamp}] {message}")

    async def highlight_element(self, page: Page, selector: str, color="red"):
        try:
            locator = page.locator(selector).first
            if await locator.is_visible():
                await locator.evaluate(f"el => el.style.border = '3px solid {color}'")
                await asyncio.sleep(0.5) # Pausa para observação humana
                await locator.evaluate("el => el.style.border = ''")
        except:
            pass

    async def run(self):
        self.log("🚀 Iniciando Teste Comportamental Supervisionado...")
        
        async with async_playwright() as p:
            # Headless=False para o usuário ver acontecendo
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
            page = await context.new_page()

            # Captura de Erros
            page.on("console", lambda msg: self.errors.append(f"CONSOLE: {msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda exc: self.errors.append(f"CRASH: {exc}"))
            page.on("response", lambda res: self.errors.append(f"HTTP {res.status}: {res.url}") if res.status >= 400 else None)

            for scenario in SCENARIOS:
                self.log(f"🎬 Cenário: {scenario['name']}")
                result = {"name": scenario['name'], "status": "PASS", "steps": []}
                
                try:
                    # Navegação
                    await page.goto(f"{BASE_URL}{scenario['url']}", wait_until="domcontentloaded")
                    await asyncio.sleep(1)
                    
                    # Identificação Visual de Elementos Interativos
                    buttons = await page.locator("button:visible").all()
                    inputs = await page.locator("input:visible").all()
                    links = await page.locator("a:visible").all()
                    
                    self.log(f"   👁️  Elementos visíveis: {len(buttons)} botões, {len(inputs)} inputs, {len(links)} links")
                    
                    # Highlight em massa (Efeito Matrix)
                    for btn in buttons[:5]: # Limita a 5 para não demorar muito
                        await btn.evaluate("el => { el.style.outline = '2px solid #ea580c'; el.style.transition = 'all 0.3s'; }")
                    await asyncio.sleep(0.5)
                    
                    # Execução de Ações Definidas
                    for action in scenario.get("actions", []):
                        selector = action["selector"]
                        self.log(f"   👉 Ação: {action['type']} em '{selector}'")
                        
                        # Highlight do alvo
                        await self.highlight_element(page, selector, "green")
                        
                        if action["type"] == "fill":
                            await page.fill(selector, action["value"])
                        elif action["type"] == "click":
                            if action.get("optional") and not await page.locator(selector).is_visible():
                                self.log("      (Item opcional não encontrado, pulando)")
                                continue
                            await page.click(selector)
                            if action.get("wait_nav"):
                                await page.wait_for_load_state("networkidle")
                        elif action["type"] == "hover":
                            await page.hover(selector)
                        
                        result["steps"].append(f"✅ {action['type']} {selector}")

                    # Screenshot de Evidência
                    shot_path = SCREENSHOT_DIR / f"{scenario['name'].replace(' ', '_')}.png"
                    await page.screenshot(path=shot_path)
                    result["screenshot"] = str(shot_path)

                except Exception as e:
                    self.log(f"   ❌ Erro no cenário: {e}")
                    result["status"] = "FAIL"
                    result["error"] = str(e)
                    self.errors.append(f"SCENARIO FAIL: {scenario['name']} - {e}")
                
                self.results.append(result)
                await asyncio.sleep(1) # Pausa entre cenários

            await browser.close()
            self.generate_report()

    def generate_report(self):
        self.log("📝 Gerando Relatório Final...")
        
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("# 🕵️ Relatório de Comportamento de UI (L6)\n")
            f.write(f"**Data:** {datetime.now().isoformat()}\n\n")
            
            f.write("## 1. Resumo dos Cenários\n")
            f.write("| Cenário | Status | Passos Executados |\n")
            f.write("| :--- | :---: | :--- |\n")
            for r in self.results:
                icon = "✅" if r["status"] == "PASS" else "❌"
                steps_count = len(r["steps"])
                f.write(f"| {r['name']} | {icon} {r['status']} | {steps_count} passos |\n")
            
            f.write("\n## 2. Erros Capturados (Console/Network)\n")
            if self.errors:
                f.write("```text\n")
                for err in self.errors:
                    f.write(f"{err}\n")
                f.write("```\n")
            else:
                f.write("✅ Nenhum erro crítico capturado durante a navegação.\n")
            
            f.write("\n## 3. Detalhamento Visual\n")
            for r in self.results:
                f.write(f"### {r['name']}\n")
                if "error" in r:
                    f.write(f"> 🚨 **Erro:** {r['error']}\n\n")
                for step in r["steps"]:
                    f.write(f"- {step}\n")
                f.write("\n")

        self.log(f"✅ Relatório salvo em: {REPORT_PATH}")

if __name__ == "__main__":
    tester = BehaviorTester()
    asyncio.run(tester.run())
