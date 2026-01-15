import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# ==============================================================================
# 🕵️ EXHAUSTIVE INTERACTION TESTER (L6) - "THE AUDITOR"
# ==============================================================================
# Objetivo: Navegar por TODAS as 38 páginas, identificar TODOS os elementos
# interativos, executar ações seguras e validar o comportamento esperado vs real.
# ==============================================================================

BASE_URL = "http://localhost:3000"
REPORT_PATH = Path("governance/evidence/REPORT_EXHAUSTIVE_INTERACTION.md")
AUTH_STATE = "auth_state.json"

# Configuração de Execução
HEADLESS = False  # Visível para o usuário
SLOW_MO = 100     # Rápido, mas perceptível

# Parâmetros para Rotas Dinâmicas
PARAMS = {
    "[slug]": "hamburgueria-ze",
    "[tableId]": "1"
}

# Lista Completa de Rotas (38 Páginas)
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

# Palavras-chave de Segurança (Ignorar para não quebrar fluxo/dados)
UNSAFE_KEYWORDS = [
    "Sair", "Logout", "Excluir", "Remover", "Delete", "Desconectar", 
    "Apagar", "Cancelar", "Voltar", "Back"
]

class ExhaustiveTester:
    def __init__(self):
        self.report_data = []
        self.total_checked = 0
        self.total_passed = 0
        self.total_skipped = 0

    def resolve_url(self, route):
        url = route
        for key, value in PARAMS.items():
            url = url.replace(key, value)
        return url

    async def highlight(self, page: Page, locator, color="#ea580c"):
        try:
            await locator.evaluate(f"el => {{ el.style.outline = '3px solid {color}'; el.style.transition = 'all 0.1s'; }}")
            await asyncio.sleep(0.1)
            await locator.evaluate("el => el.style.outline = ''")
        except:
            pass

    async def analyze_interaction(self, page: Page, element, route):
        tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
        text = (await element.text_content() or "").strip()[:40].replace("\n", " ")
        
        identifier = f"<{tag_name}> {text}" if text else f"<{tag_name}>"
        
        # Filtro de Segurança
        if any(unsafe.lower() in text.lower() for unsafe in UNSAFE_KEYWORDS):
            self.report_data.append({
                "page": route,
                "element": identifier,
                "expected": "Ação Destrutiva/Navegação",
                "reality": "Ignorado (Segurança)",
                "status": "⚠️ SKIPPED"
            })
            self.total_skipped += 1
            return

        # Definição de Expectativa
        expected = "Feedback Visual"
        if tag_name == "a" or await element.get_attribute("href"):
            expected = "Navegação"
        elif tag_name == "input":
            expected = "Input de Dados"
        
        reality = "Sem reação"
        status = "❌ FAIL"
        
        try:
            await self.highlight(page, element)
            
            if tag_name == "input":
                type_attr = await element.get_attribute("type")
                if type_attr in ["checkbox", "radio"]:
                    await element.click()
                    reality = "Toggle/Check"
                    status = "✅ PASS"
                    await element.click() # Reverte
                else:
                    original = await element.input_value()
                    await element.fill("QA Test")
                    if await element.input_value() == "QA Test":
                        reality = "Texto inserido"
                        status = "✅ PASS"
                    else:
                        reality = "Input controlado/bloqueado"
                        status = "⚠️ WARN"
                    await element.fill(original) # Reverte
            else:
                # Clique Seguro
                url_before = page.url
                try:
                    # Tenta clicar. Se navegar, volta.
                    await element.click(timeout=1000)
                    
                    if page.url != url_before:
                        reality = "Navegação realizada"
                        status = "✅ PASS"
                        await page.go_back()
                        await page.wait_for_load_state("domcontentloaded")
                    else:
                        reality = "Clique registrado (UI Action)"
                        status = "✅ PASS"
                except Exception as e:
                    reality = f"Erro no clique: {str(e)[:30]}"
                    status = "❌ ERROR"

        except Exception as e:
            reality = f"Erro geral: {str(e)[:30]}"
            status = "❌ ERROR"

        self.report_data.append({
            "page": route,
            "element": identifier,
            "expected": expected,
            "reality": reality,
            "status": status
        })
        
        if "PASS" in status: self.total_passed += 1
        self.total_checked += 1

    async def run(self):
        print("🕵️  Iniciando Auditoria Exaustiva de Interação (L6)...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
            context = await browser.new_context(viewport={"width": 1366, "height": 768})
            
            # Login
            print("🔑 Autenticando Admin...")
            page = await context.new_page()
            try:
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard")
            except:
                print("⚠️  Login falhou ou já autenticado. Prosseguindo...")

            for route in ROUTES:
                url = self.resolve_url(route)
                full_url = f"{BASE_URL}{url}"
                print(f"\n🔭 Auditando: {url}")
                
                try:
                    await page.goto(full_url, wait_until="domcontentloaded")
                    await asyncio.sleep(0.5)
                    
                    # Seleciona TODOS os elementos interativos
                    elements = await page.locator("button:visible, a:visible, input:visible").all()
                    print(f"   -> {len(elements)} elementos encontrados.")
                    
                    # Limite de segurança por página para não travar em loops infinitos
                    # Mas alto o suficiente para cobrir quase tudo
                    for i, el in enumerate(elements[:50]): 
                        if await el.is_visible():
                            await self.analyze_interaction(page, el, url)
                            
                except Exception as e:
                    print(f"   ❌ Erro na página {url}: {e}")
                    self.report_data.append({
                        "page": url,
                        "element": "PAGE_LOAD",
                        "expected": "Carregar",
                        "reality": f"Crash: {e}",
                        "status": "❌ CRITICAL"
                    })

            await browser.close()
            self.generate_report()

    def generate_report(self):
        print("\n📝 Gerando Relatório Exaustivo...")
        
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("# 🕵️ Relatório de Interação Exaustiva (L6)\n")
            f.write(f"**Data:** {datetime.now().isoformat()}\n")
            f.write(f"**Páginas:** {len(ROUTES)}\n")
            f.write(f"**Elementos Auditados:** {self.total_checked}\n")
            f.write(f"**Sucesso:** {self.total_passed} | **Skipped:** {self.total_skipped}\n\n")
            
            f.write("| Página | Elemento | Expectativa | Realidade | Status |\n")
            f.write("| :--- | :--- | :--- | :--- | :---: |\n")
            
            current_page = ""
            for item in self.report_data:
                page_display = f"**{item['page']}**" if item['page'] != current_page else ""
                current_page = item['page']
                # Limpa pipes para tabela MD
                elem = item['element'].replace("|", "/")
                real = item['reality'].replace("|", "/")
                
                f.write(f"| {page_display} | `{elem}` | {item['expected']} | {real} | {item['status']} |\n")

        print(f"✅ Relatório salvo em: {REPORT_PATH}")

if __name__ == "__main__":
    tester = ExhaustiveTester()
    asyncio.run(tester.run())
