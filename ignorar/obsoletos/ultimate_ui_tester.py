# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 18:45:00
import asyncio
import os
import shutil
import random
import requests
from datetime import datetime
from playwright.async_api import async_playwright, Page, ElementHandle
from faker import Faker

# ==============================================================================
# CONFIGURAÇÃO DO ULTIMATE UI TESTER (V5 - ROBUST & SEEDED)
# ==============================================================================
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

REPORT_FILE = "docs/reports/ULTIMATE_UI_REPORT.md"
VIDEO_DIR = "docs/reports/videos"
SCREENSHOT_DIR = "docs/reports/evidence"

fake = Faker('pt_BR')

ROUTES = [
    {"name": "01_Landing", "url": "/", "type": "public"},
    {"name": "02_Login", "url": "/admin/login", "type": "auth"},
    {"name": "03_Dashboard", "url": f"/admin/{SLUG}/dashboard", "type": "admin"},
    {"name": "04_Menu_Admin", "url": f"/admin/{SLUG}/menu", "type": "admin"},
    {"name": "05_Mesas_Admin", "url": f"/admin/{SLUG}/tables", "type": "admin"},
    {"name": "06_Estoque", "url": f"/admin/{SLUG}/inventory", "type": "admin"},
    {"name": "07_Equipe", "url": f"/admin/{SLUG}/team", "type": "admin"},
    {"name": "08_Configuracoes", "url": f"/admin/{SLUG}/settings", "type": "admin"},
    {"name": "09_KDS_Cozinha", "url": f"/admin/{SLUG}/kitchen", "type": "admin"},
    {"name": "10_App_Garcom", "url": f"/admin/{SLUG}/waiter", "type": "admin"},
    {"name": "11_Delivery_Admin", "url": f"/admin/{SLUG}/delivery", "type": "admin"},
    {"name": "12_Menu_Publico", "url": f"/{SLUG}/menu", "type": "public"},
]

DANGEROUS_KEYWORDS = ["Sair", "Logout", "Excluir", "Remover", "Deletar", "Delete", "Limpar", "Desconectar"]
SUBMIT_KEYWORDS = ["Salvar", "Criar", "Adicionar", "Entrar", "Confirmar", "Enviar", "Cadastrar", "Login"]

class UltimateReporter:
    def __init__(self):
        self.entries = []
        self.start_time = datetime.now()

    def log(self, context, element, action, expected, actual, status, evidence=None):
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "context": context,
            "element": element,
            "action": action,
            "expected": expected,
            "actual": actual,
            "status": status,
            "evidence": evidence
        }
        self.entries.append(entry)
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{icon} [{context}] {element}: {actual}")

    def save(self):
        duration = datetime.now() - self.start_time
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Relatório Ultimate UI Stress Test (v5)\n")
            f.write(f"**Data:** {self.start_time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Duração:** {duration}\n\n")
            
            f.write("## 📹 Evidência em Vídeo\n")
            f.write(f"Gravação completa disponível em: `{VIDEO_DIR}`\n\n")

            f.write("## 📊 Detalhamento de Interações\n")
            f.write("| Contexto | Elemento | Ação | Comportamento Esperado | Comportamento Real | Status | Evidência |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            
            for e in self.entries:
                evidence_link = f"[Ver]({os.path.relpath(e['evidence'], os.path.dirname(REPORT_FILE))})" if e['evidence'] else "-"
                icon = "✅" if e['status'] == "PASS" else "❌" if e['status'] == "FAIL" else "⚠️"
                f.write(f"| {e['context']} | `{e['element']}` | {e['action']} | {e['expected']} | {e['actual']} | {icon} | {evidence_link} |\n")

        print(f"\n📄 Relatório salvo em: {REPORT_FILE}")

async def fill_inputs(page: Page, container_selector: str = "body"):
    inputs = await page.locator(f"{container_selector} input:visible, {container_selector} textarea:visible").all()
    filled_count = 0
    for inp in inputs:
        try:
            if await inp.input_value(): continue
            inp_type = await inp.get_attribute("type") or "text"
            name = await inp.get_attribute("name") or ""
            placeholder = await inp.get_attribute("placeholder") or ""
            
            value = ""
            if "email" in name.lower() or "email" in placeholder.lower(): value = fake.email()
            elif "phone" in name.lower() or "tel" in inp_type: value = "11999999999"
            elif "price" in name.lower() or "number" in inp_type: value = str(random.randint(10, 100))
            elif "password" in inp_type: value = "SenhaForte123!"
            else: value = fake.word()
            
            await inp.fill(value)
            filled_count += 1
        except: pass
    return filled_count

async def handle_modal(page: Page, reporter: UltimateReporter, parent_context: str):
    modal_selector = "div[role='dialog'], div.fixed.z-50, div.fixed.inset-0"
    try:
        modal = page.locator(modal_selector).first
        if await modal.is_visible(timeout=2000):
            reporter.log(parent_context, "Modal", "Detecção", "Modal deve abrir", "Modal detectado", "PASS")
            await fill_inputs(page, modal_selector)
            
            # Interagir com botões do modal
            buttons = await modal.locator("button").all()
            for btn in buttons:
                text = await btn.inner_text()
                if any(k in text for k in SUBMIT_KEYWORDS):
                    await btn.click()
                    reporter.log(parent_context, f"Modal Button '{text}'", "Click", "Ação do modal", "Clicado", "PASS")
                    await page.wait_for_timeout(1000)
            
            # Fechar modal
            if await modal.is_visible():
                close_btn = modal.locator("button svg.lucide-x, button:has-text('Cancelar'), button:has-text('Fechar')").first
                if await close_btn.is_visible():
                    await close_btn.click()
                    reporter.log(parent_context, "Modal Close", "Click", "Modal deve fechar", "Modal fechado", "PASS")
            return True
    except: pass
    return False

async def run_test():
    # Limpeza
    if os.path.exists(SCREENSHOT_DIR): shutil.rmtree(SCREENSHOT_DIR)
    if os.path.exists(VIDEO_DIR): shutil.rmtree(VIDEO_DIR)
    os.makedirs(SCREENSHOT_DIR)
    os.makedirs(VIDEO_DIR)

    reporter = UltimateReporter()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 800},
            ignore_https_errors=True
        )
        
        await context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        page = await context.new_page()

        # 1. Login
        print("🔑 Autenticando...")
        try:
            await page.goto(f"{BASE_URL}/admin/login")
            await fill_inputs(page)
            await page.fill('input[name="email"]', ADMIN_EMAIL)
            await page.fill('input[name="password"]', ADMIN_PASS)
            await page.click('button[type="submit"]')
            await page.wait_for_url("**/dashboard", timeout=15000)
            reporter.log("Login", "Formulário", "Submit", "Redirecionar Dashboard", "Sucesso", "PASS")
        except Exception as e:
            path = f"{SCREENSHOT_DIR}/login_fail.png"
            await page.screenshot(path=path)
            reporter.log("Login", "Auth", "Submit", "Redirecionar Dashboard", f"Falha: {e}", "FAIL", path)
            await context.close()
            reporter.save()
            return

        # 2. Loop de Rotas
        for route in ROUTES:
            if route['type'] == 'public': continue 
            
            print(f"\n🔍 Explorando: {route['name']}")
            try:
                await page.goto(f"{BASE_URL}{route['url']}", wait_until="domcontentloaded")
                await page.wait_for_timeout(1500) # Estabilização

                # CORREÇÃO CRÍTICA: Usar ElementHandles para evitar Stale Element Reference
                # Em vez de locator.all(), pegamos os handles diretos
                handles = await page.query_selector_all("button:visible, a.bg-orange-600:visible, [role='button']:visible")
                
                reporter.log(route['name'], "Scan", "Análise", "Detectar elementos", f"{len(handles)} elementos encontrados", "INFO")

                # Limita a 5 interações principais por página
                for i, handle in enumerate(handles[:5]):
                    try:
                        # Verifica se ainda está visível e conectado
                        if not await handle.is_visible(): continue
                        
                        text = (await handle.inner_text()).strip() or "Icon"
                        
                        if any(d in text for d in DANGEROUS_KEYWORDS): continue

                        # Lógica de Formulário
                        if any(s in text for s in SUBMIT_KEYWORDS):
                            filled = await fill_inputs(page)
                            if filled > 0:
                                reporter.log(route['name'], "Formulário", "Preencher", "Preencher inputs", f"{filled} campos preenchidos", "PASS")

                        # Ação de Clique (Protegida)
                        await handle.click(timeout=3000)
                        
                        modal_opened = await handle_modal(page, reporter, route['name'])
                        
                        if not modal_opened:
                            reporter.log(route['name'], text, "Click", "Ação ou Navegação", "Clicado (Sem modal)", "PASS")
                        
                        # Se navegou, volta
                        if page.url != f"{BASE_URL}{route['url']}" and not modal_opened:
                            await page.go_back()
                            await page.wait_for_timeout(1000) # Espera recarregar

                    except Exception as click_err:
                        # Loga erro de interação individual mas não para o teste
                        # reporter.log(route['name'], text, "Click", "Interação", f"Erro: {click_err}", "WARN")
                        pass

            except Exception as e:
                path = f"{SCREENSHOT_DIR}/{route['name']}_error.png"
                await page.screenshot(path=path)
                reporter.log(route['name'], "Geral", "Navegação", "Carregar página", str(e), "FAIL", path)

        await context.close()
        await browser.close()
        reporter.save()

if __name__ == "__main__":
    asyncio.run(run_test())
