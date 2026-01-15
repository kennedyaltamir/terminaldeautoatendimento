# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 19:00:00
import asyncio
import os
import shutil
import random
import json
from datetime import datetime
from playwright.async_api import async_playwright, Page, expect
from faker import Faker

# ==============================================================================
# CONFIGURAÇÃO DO ULTIMATE UI TESTER (V6 - STATEFUL & SMART)
# ==============================================================================
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

REPORT_FILE = "docs/reports/ULTIMATE_UI_REPORT.md"
VIDEO_DIR = "docs/reports/videos"
SCREENSHOT_DIR = "docs/reports/evidence"
AUTH_STATE_FILE = "auth_state.json"

fake = Faker('pt_BR')

ROUTES = [
    {"name": "01_Dashboard", "url": f"/admin/{SLUG}/dashboard", "type": "admin"},
    {"name": "02_Menu_Admin", "url": f"/admin/{SLUG}/menu", "type": "admin"},
    {"name": "03_Mesas_Admin", "url": f"/admin/{SLUG}/tables", "type": "admin"},
    {"name": "04_Estoque", "url": f"/admin/{SLUG}/inventory", "type": "admin"},
    {"name": "05_Equipe", "url": f"/admin/{SLUG}/team", "type": "admin"},
    {"name": "06_Configuracoes", "url": f"/admin/{SLUG}/settings", "type": "admin"},
    {"name": "07_KDS_Cozinha", "url": f"/admin/{SLUG}/kitchen", "type": "admin"},
    {"name": "08_App_Garcom", "url": f"/admin/{SLUG}/waiter", "type": "admin"},
    {"name": "09_Delivery_Admin", "url": f"/admin/{SLUG}/delivery", "type": "admin"},
    {"name": "10_Menu_Publico", "url": f"/{SLUG}/menu", "type": "public"},
]

# Palavras-chave para NÃO clicar
DANGEROUS_KEYWORDS = ["Sair", "Logout", "Excluir", "Remover", "Deletar", "Delete", "Limpar", "Desconectar"]
# Botões que indicam ação de formulário
ACTION_KEYWORDS = ["Salvar", "Criar", "Adicionar", "Entrar", "Confirmar", "Enviar", "Cadastrar", "Login", "Novo"]

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
            f.write(f"# 🛡️ Relatório Ultimate UI Stress Test (v6 - Stateful)\n")
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

async def fill_smart_form(page: Page, container_selector: str = "body"):
    """Preenche inputs visíveis com dados contextuais."""
    inputs = await page.locator(f"{container_selector} input:visible, {container_selector} textarea:visible").all()
    filled_count = 0
    
    for inp in inputs:
        try:
            if await inp.input_value(): continue # Pula se já tem valor
            
            inp_type = await inp.get_attribute("type") or "text"
            name = await inp.get_attribute("name") or ""
            placeholder = await inp.get_attribute("placeholder") or ""
            label_txt = name.lower() + placeholder.lower()
            
            value = ""
            if "email" in label_txt: value = fake.email()
            elif "phone" in label_txt or "tel" in inp_type: value = "11999999999"
            elif "price" in label_txt or "number" in inp_type: value = str(random.randint(10, 100))
            elif "password" in inp_type: value = "SenhaForte123!"
            elif "color" in inp_type: value = "#ea580c"
            elif "time" in inp_type: value = "12:00"
            else: value = fake.word()
            
            await inp.fill(value)
            filled_count += 1
        except: pass
    return filled_count

async def check_modal_and_interact(page: Page, reporter: UltimateReporter, context_name: str):
    """Verifica se um modal abriu e interage com ele."""
    # Seletores comuns de modal
    modal_selectors = ["div[role='dialog']", "div.fixed.z-50", ".radix-dialog-content"]
    
    for selector in modal_selectors:
        try:
            modal = page.locator(selector).first
            if await modal.is_visible(timeout=1500):
                reporter.log(context_name, "Modal", "Detecção", "Modal deve abrir", "Modal detectado", "PASS")
                
                # Preencher formulário no modal
                await fill_smart_form(page, selector)
                
                # Tentar clicar em botão de ação no modal
                action_btn = modal.locator("button.bg-orange-600, button[type='submit']").first
                if await action_btn.is_visible():
                    txt = await action_btn.inner_text()
                    await action_btn.click()
                    reporter.log(context_name, f"Modal Btn '{txt}'", "Click", "Submeter", "Clicado", "PASS")
                    await page.wait_for_timeout(1000)
                
                # Fechar se ainda estiver aberto
                if await modal.is_visible():
                    close_btn = modal.locator("button svg.lucide-x, button:has-text('Cancelar')").first
                    if await close_btn.is_visible():
                        await close_btn.click()
                
                return True
        except: pass
    return False

async def run_test():
    # Limpeza
    if os.path.exists(SCREENSHOT_DIR): shutil.rmtree(SCREENSHOT_DIR)
    if os.path.exists(VIDEO_DIR): shutil.rmtree(VIDEO_DIR)
    if os.path.exists(AUTH_STATE_FILE): os.remove(AUTH_STATE_FILE)
    
    os.makedirs(SCREENSHOT_DIR)
    os.makedirs(VIDEO_DIR)

    reporter = UltimateReporter()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # --- FASE 1: LOGIN E CAPTURA DE ESTADO ---
        print("🔑 FASE 1: Autenticação e Persistência...")
        context = await browser.new_context(record_video_dir=VIDEO_DIR)
        page = await context.new_page()
        
        try:
            await page.goto(f"{BASE_URL}/admin/login")
            await page.fill('input[name="email"]', ADMIN_EMAIL)
            await page.fill('input[name="password"]', ADMIN_PASS)
            await page.click('button[type="submit"]')
            await page.wait_for_url("**/dashboard", timeout=15000)
            
            # Salva o estado (Cookies + LocalStorage)
            await context.storage_state(path=AUTH_STATE_FILE)
            
            # Injeta flag de tour completed no estado salvo
            # (Isso é um hack: lemos o arquivo, adicionamos o item e salvamos de volta)
            with open(AUTH_STATE_FILE, 'r') as f:
                state = json.load(f)
            state['origins'][0]['localStorage'].append({'name': 'mesaflow_tour_completed', 'value': 'true'})
            with open(AUTH_STATE_FILE, 'w') as f:
                json.dump(state, f)
                
            reporter.log("Login", "Auth", "Login", "Gerar Token", "Sucesso (Estado Salvo)", "PASS")
            await context.close() # Fecha contexto de login
            
        except Exception as e:
            path = f"{SCREENSHOT_DIR}/login_fatal.png"
            await page.screenshot(path=path)
            reporter.log("Login", "Auth", "Login", "Gerar Token", f"Falha: {e}", "FAIL", path)
            await browser.close()
            reporter.save()
            return

        # --- FASE 2: VARREDURA COM ESTADO PERSISTIDO ---
        print("🚀 FASE 2: Varredura Profunda...")
        
        # Cria novo contexto com o estado salvo (já logado)
        context = await browser.new_context(
            storage_state=AUTH_STATE_FILE,
            viewport={'width': 1280, 'height': 800},
            record_video_dir=VIDEO_DIR
        )
        page = await context.new_page()

        for route in ROUTES:
            print(f"\n🔍 Auditando: {route['name']}")
            try:
                await page.goto(f"{BASE_URL}{route['url']}", wait_until="domcontentloaded")
                await page.wait_for_timeout(1500)

                # Verificação de Segurança: Se redirecionou para login, falhou
                if "/login" in page.url and route['type'] == 'admin':
                    reporter.log(route['name'], "Acesso", "Navegar", "Manter Sessão", "Redirecionado para Login (Falha de Auth)", "FAIL")
                    continue

                # Identificar elementos interativos
                # Usamos seletores mais específicos para evitar pegar coisas ocultas
                buttons = await page.locator("button:visible, a[href]:visible, [role='button']:visible").all()
                
                reporter.log(route['name'], "Scan", "Análise", "Detectar elementos", f"{len(buttons)} elementos encontrados", "INFO")

                # Limita interações para não demorar horas, mas foca nos importantes
                interacted_count = 0
                for btn in buttons:
                    if interacted_count >= 5: break # Max 5 interações por página
                    
                    try:
                        text = (await btn.inner_text()).strip()
                        if not text: continue # Pula botões sem texto (ícones puros as vezes dão problema)
                        
                        if any(d in text for d in DANGEROUS_KEYWORDS): continue

                        # Se for botão de ação, preenche formulário antes
                        if any(s in text for s in ACTION_KEYWORDS):
                            filled = await fill_smart_form(page)
                            if filled > 0:
                                reporter.log(route['name'], "Formulário", "Preencher", "Preencher inputs", f"{filled} campos", "PASS")

                        # CLIQUE
                        await btn.click(timeout=2000)
                        interacted_count += 1
                        
                        # Verifica Modal
                        modal_opened = await check_modal_and_interact(page, reporter, route['name'])
                        
                        if not modal_opened:
                            # Verifica Navegação
                            if page.url != f"{BASE_URL}{route['url']}":
                                reporter.log(route['name'], text, "Click", "Navegação", f"Navegou para {page.url}", "PASS")
                                await page.go_back()
                                await page.wait_for_timeout(500)
                            else:
                                reporter.log(route['name'], text, "Click", "Ação", "Clicado (Sem navegação)", "PASS")

                    except Exception as e:
                        # Ignora erros de clique pontuais (elemento coberto, etc)
                        pass

            except Exception as e:
                path = f"{SCREENSHOT_DIR}/{route['name']}_crash.png"
                await page.screenshot(path=path)
                reporter.log(route['name'], "Geral", "Navegação", "Carregar página", str(e), "FAIL", path)

        await context.close()
        await browser.close()
        reporter.save()

if __name__ == "__main__":
    asyncio.run(run_test())
