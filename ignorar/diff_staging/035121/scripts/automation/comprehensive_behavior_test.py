import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, expect

# ==============================================================================
# 🕵️ COMPREHENSIVE BEHAVIOR TESTER v2.0 (Deep Crawler)
# ==============================================================================
# Objetivo: Navegar por TODAS as telas, lidar com modais (Onboarding),
# interagir com elementos e validar comportamento real vs esperado.
# ==============================================================================

BASE_URL = "http://localhost:3000"
REPORT_PATH = Path("governance/evidence/REPORT_BEHAVIOR_TEST.md")
SCREENSHOT_DIR = Path("testesvisuais/behavior")

# Configuração de Cenários Expandida
SCENARIOS = [
    {
        "name": "1. Login Admin",
        "url": "/admin/login",
        "actions": [
            {"type": "fill", "selector": "input[name='email']", "value": "admin@mesaflow.com"},
            {"type": "fill", "selector": "input[name='password']", "value": "123456"},
            {"type": "click", "selector": "button[type='submit']", "wait_nav": True}
        ]
    },
    {
        "name": "2. Onboarding & Dashboard",
        "url": "/admin/hamburgueria-ze/dashboard",
        "actions": [
            # Tratamento do Tour (Joyride)
            {"type": "click", "selector": "button[aria-label='Pular tour']", "optional": True, "desc": "Fechar Tour"},
            {"type": "click", "selector": "button:has-text('Fechar')", "optional": True, "desc": "Fechar Modal Genérico"},
            # Interações Dashboard
            {"type": "hover", "selector": "text=Faturamento"},
            {"type": "hover", "selector": "text=Ticket Médio"},
            {"type": "click", "selector": "button:has-text('Hoje')", "desc": "Filtro Hoje"},
            {"type": "click", "selector": "button:has-text('7 Dias')", "desc": "Filtro 7 Dias"}
        ]
    },
    {
        "name": "3. Gestão de Cardápio",
        "url": "/admin/hamburgueria-ze/menu",
        "actions": [
            {"type": "click", "selector": "button:has-text('Criar Categoria')", "expect_modal": True},
            {"type": "fill", "selector": "input[placeholder='Nome da Categoria']", "value": "Teste Auto", "optional": True},
            {"type": "click", "selector": "button:has-text('Cancelar')", "desc": "Fechar Modal Categoria"},
            # Expandir um produto se existir
            {"type": "click", "selector": "button:has(svg.lucide-chevron-down)", "optional": True, "desc": "Expandir Produto"}
        ]
    },
    {
        "name": "4. Gestão de Mesas",
        "url": "/admin/hamburgueria-ze/tables",
        "actions": [
            {"type": "click", "selector": "button:has-text('Criar a primeira mesa')", "optional": True},
            {"type": "click", "selector": "button:has-text('Gerar')", "optional": True},
            {"type": "click", "selector": "button:has-text('Cancelar')", "optional": True}
        ]
    },
    {
        "name": "5. KDS (Cozinha)",
        "url": "/admin/hamburgueria-ze/kitchen",
        "actions": [
            {"type": "click", "selector": "button[title='Tela Cheia']", "desc": "Toggle Fullscreen"},
            {"type": "click", "selector": "button[title='Resumo (A)']", "desc": "Abrir Resumo"},
            {"type": "click", "selector": "button:has(svg.lucide-x)", "desc": "Fechar Resumo", "optional": True},
            {"type": "click", "selector": "button:has-text('Cozinha')", "desc": "Filtro Cozinha"},
            {"type": "click", "selector": "button:has-text('Bar')", "desc": "Filtro Bar"}
        ]
    },
    {
        "name": "6. Garçom (POS)",
        "url": "/admin/hamburgueria-ze/waiter",
        "actions": [
            {"type": "click", "selector": "button:has-text('Livre')", "desc": "Filtro Livre"},
            {"type": "click", "selector": "button:has-text('Ocupada')", "desc": "Filtro Ocupada"},
            {"type": "click", "selector": "a[href*='/waiter/orders']", "desc": "Aba Pedidos"}
        ]
    },
    {
        "name": "7. Estoque",
        "url": "/admin/hamburgueria-ze/inventory",
        "actions": [
            {"type": "click", "selector": "button:has-text('Novo Ingrediente')", "expect_modal": True},
            {"type": "click", "selector": "button:has-text('Cancelar')", "desc": "Fechar Modal"}
        ]
    },
    {
        "name": "8. Configurações",
        "url": "/admin/hamburgueria-ze/settings",
        "actions": [
            {"type": "fill", "selector": "input[name='name']", "value": "Hamburgueria Zé (Auto)"},
            {"type": "click", "selector": "button:has-text('Salvar Alterações')"}
        ]
    },
    {
        "name": "9. Menu Público (Cliente)",
        "url": "/hamburgueria-ze/menu",
        "actions": [
            # Simula cliente
            {"type": "click", "selector": "div[role='button']:has-text('X-Bacon')", "desc": "Abrir Produto", "wait_for": "text=Adicionar ao Carrinho"},
            {"type": "click", "selector": "button:has(svg.lucide-plus)", "desc": "Aumentar Qtd", "repeat": 2},
            {"type": "fill", "selector": "textarea", "value": "Sem cebola, capricha no bacon!"},
            {"type": "click", "selector": "button:has-text('Adicionar ao Carrinho')", "desc": "Add Cart"},
            {"type": "click", "selector": "button:has-text('Ver Carrinho')", "desc": "Open Cart"},
            {"type": "click", "selector": "button:has-text('Voltar')", "desc": "Close Cart"}
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
                await locator.evaluate(f"el => el.style.outline = '3px solid {color}'")
                await asyncio.sleep(0.3)
                await locator.evaluate("el => el.style.outline = ''")
        except:
            pass

    async def handle_onboarding(self, page: Page):
        """Tenta fechar modais de tour ou boas-vindas."""
        try:
            # Joyride Skip Button
            skip_btn = page.locator("button[aria-label='Pular tour']")
            if await skip_btn.is_visible(timeout=2000):
                self.log("   👋 Tour detectado. Fechando...")
                await skip_btn.click()
                await asyncio.sleep(0.5)
            
            # Generic Close Button in Modals
            close_btn = page.locator("button:has(svg.lucide-x)").first
            if await close_btn.is_visible(timeout=1000):
                # Cuidado para não fechar algo importante, mas no boot geralmente é modal
                pass 
        except:
            pass

    async def run(self):
        self.log("🚀 Iniciando Teste Comportamental Completo (L6)...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=500)
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                record_video_dir="testesvisuais/videos"
            )
            page = await context.new_page()

            # Listeners de Erro
            page.on("console", lambda msg: self.errors.append(f"CONSOLE: {msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda exc: self.errors.append(f"CRASH: {exc}"))
            page.on("response", lambda res: self.errors.append(f"HTTP {res.status}: {res.url}") if res.status >= 400 else None)

            for scenario in SCENARIOS:
                self.log(f"\n🎬 Cenário: {scenario['name']}")
                result = {"name": scenario['name'], "status": "PASS", "steps": []}
                
                try:
                    # Navegação
                    await page.goto(f"{BASE_URL}{scenario['url']}", wait_until="domcontentloaded")
                    await asyncio.sleep(1.5) # Wait for hydration
                    
                    # Tratamento Especial: Onboarding no Dashboard
                    if "Dashboard" in scenario['name']:
                        await self.handle_onboarding(page)

                    # Scan Visual
                    buttons = await page.locator("button:visible").all()
                    inputs = await page.locator("input:visible").all()
                    self.log(f"   👁️  Visíveis: {len(buttons)} botões, {len(inputs)} inputs")

                    # Execução de Ações
                    for action in scenario.get("actions", []):
                        selector = action["selector"]
                        desc = action.get("desc", selector)
                        
                        # Verifica visibilidade antes de interagir
                        try:
                            locator = page.locator(selector).first
                            if not await locator.is_visible(timeout=3000):
                                if action.get("optional"):
                                    self.log(f"      ⚠️  Opcional não encontrado: {desc}")
                                    continue
                                else:
                                    raise Exception(f"Elemento não visível: {selector}")
                            
                            self.log(f"   👉 Ação: {action['type']} em '{desc}'")
                            await self.highlight_element(page, selector, "#ea580c")
                            
                            if action["type"] == "fill":
                                await locator.fill(action["value"])
                            elif action["type"] == "click":
                                await locator.click()
                                if action.get("wait_nav"):
                                    await page.wait_for_load_state("networkidle")
                                if action.get("wait_for"):
                                    await page.wait_for_selector(action["wait_for"], timeout=5000)
                            elif action["type"] == "hover":
                                await locator.hover()
                            
                            result["steps"].append(f"✅ {desc}")
                            
                        except Exception as e:
                            self.log(f"      ❌ Falha na ação '{desc}': {str(e)[:100]}...")
                            if not action.get("optional"):
                                raise e

                    # Screenshot Final do Cenário
                    shot_path = SCREENSHOT_DIR / f"{scenario['name'].split('.')[0].strip().replace(' ', '_')}.png"
                    await page.screenshot(path=shot_path)
                    result["screenshot"] = str(shot_path)

                except Exception as e:
                    self.log(f"   🔥 CRITICAL FAIL: {e}")
                    result["status"] = "FAIL"
                    result["error"] = str(e)
                    self.errors.append(f"SCENARIO {scenario['name']}: {e}")
                
                self.results.append(result)

            await browser.close()
            self.generate_report()

    def generate_report(self):
        self.log("\n📝 Gerando Relatório Final...")
        
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("# 🕵️ Relatório de Comportamento de UI (L6 - Full Coverage)\n")
            f.write(f"**Data:** {datetime.now().isoformat()}\n\n")
            
            f.write("## 1. Resumo dos Cenários\n")
            f.write("| Cenário | Status | Passos |\n")
            f.write("| :--- | :---: | :--- |\n")
            for r in self.results:
                icon = "✅" if r["status"] == "PASS" else "❌"
                f.write(f"| {r['name']} | {icon} {r['status']} | {len(r['steps'])} |\n")
            
            f.write("\n## 2. Erros Capturados\n")
            if self.errors:
                f.write("```text\n")
                for err in self.errors:
                    f.write(f"{err}\n")
                f.write("```\n")
            else:
                f.write("✅ Sistema estável. Nenhum erro crítico capturado.\n")
            
            f.write("\n## 3. Detalhamento\n")
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
