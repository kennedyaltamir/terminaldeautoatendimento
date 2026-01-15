# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 18:00:00
import asyncio
import os
import time
import shutil
from datetime import datetime
from playwright.async_api import async_playwright, Page, BrowserContext

# ==============================================================================
# CONFIGURAÇÃO DO TESTE DE ESTRESSE DE UI (V2 - EXPLORATORY)
# ==============================================================================
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"
REPORT_FILE = "docs/reports/FULL_UI_TEST_REPORT.md"
VIDEO_DIR = "docs/reports/videos"
SCREENSHOT_DIR = "docs/reports/evidence"

# Rotas para auditar (Cobre todos os módulos do sistema)
ROUTES = [
    {"name": "01_Landing", "url": "/", "public": True},
    {"name": "02_Login", "url": "/admin/login", "public": True},
    {"name": "03_Dashboard", "url": f"/admin/{SLUG}/dashboard"},
    {"name": "04_Menu_Admin", "url": f"/admin/{SLUG}/menu"},
    {"name": "05_Mesas_Admin", "url": f"/admin/{SLUG}/tables"},
    {"name": "06_Estoque", "url": f"/admin/{SLUG}/inventory"},
    {"name": "07_Equipe", "url": f"/admin/{SLUG}/team"},
    {"name": "08_Configuracoes", "url": f"/admin/{SLUG}/settings"},
    {"name": "09_KDS_Cozinha", "url": f"/admin/{SLUG}/kitchen"},
    {"name": "10_App_Garcom", "url": f"/admin/{SLUG}/waiter"},
    {"name": "11_Delivery_Admin", "url": f"/admin/{SLUG}/delivery"},
    {"name": "12_Menu_Publico", "url": f"/{SLUG}/menu", "public": True},
]

# Palavras-chave para NÃO clicar (Evitar logout ou destruição de dados)
DANGEROUS_KEYWORDS = ["Sair", "Logout", "Excluir", "Remover", "Deletar", "Delete", "Limpar", "Desconectar"]

class TestReporter:
    def __init__(self):
        self.logs = []
        self.errors = []
        self.start_time = datetime.now()

    def log_interaction(self, page_name, element_text, result, details=""):
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "page": page_name,
            "element": element_text,
            "result": result,
            "details": details
        }
        self.logs.append(entry)
        print(f"[{entry['result']}] {page_name} -> '{element_text}': {details}")

    def log_error(self, page_name, error_msg, screenshot_path=None):
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "page": page_name,
            "error": error_msg,
            "screenshot": screenshot_path
        }
        self.errors.append(entry)
        print(f"❌ ERRO em {page_name}: {error_msg}")

    def save_report(self):
        duration = datetime.now() - self.start_time
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Relatório de Teste de Interface Abrangente (UI Stress Test v2)\n")
            f.write(f"**Data:** {self.start_time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Duração:** {duration}\n")
            f.write(f"**Total de Interações:** {len(self.logs)}\n")
            f.write(f"**Total de Erros:** {len(self.errors)}\n\n")
            
            f.write("## 📹 Evidência em Vídeo\n")
            f.write("Os vídeos da execução foram salvos em `docs/reports/videos/`.\n\n")

            if self.errors:
                f.write("## 🚨 Erros Críticos Encontrados\n")
                for err in self.errors:
                    f.write(f"- **{err['page']}**: {err['error']}\n")
                    if err['screenshot']:
                        rel_path = os.path.relpath(err['screenshot'], os.path.dirname(REPORT_FILE))
                        f.write(f"  - Evidência: ![{err['page']}]({rel_path})\n")
                f.write("\n")
            
            f.write("## 📝 Log de Interações\n")
            f.write("| Página | Elemento / Ação | Resultado | Detalhes |\n")
            f.write("|---|---|---|---|\n")
            for log in self.logs:
                icon = "✅" if log['result'] == "SUCCESS" else "⚠️" if log['result'] == "SKIPPED" else "❌"
                f.write(f"| {log['page']} | `{log['element']}` | {icon} {log['result']} | {log['details']} |\n")
        
        print(f"\n📄 Relatório salvo em: {REPORT_FILE}")

async def handle_onboarding_tour(page: Page):
    """
    Tenta fechar o tour do Joyride se ele aparecer, ou injeta o localStorage para prevenir.
    """
    # Estratégia 1: Prevenção via LocalStorage
    await page.add_init_script("""
        window.localStorage.setItem('mesaflow_tour_completed', 'true');
    """)
    
    # Estratégia 2: Clique no botão de fechar/pular se aparecer
    try:
        tour_close = page.locator("button[aria-label='Close'], button:has-text('Pular'), button:has-text('Fechar')").first
        if await tour_close.is_visible(timeout=2000):
            await tour_close.click()
            return True
    except:
        pass
    return False

async def explore_page(page: Page, route_name: str, reporter: TestReporter):
    """
    Explora uma página identificando elementos interativos e verificando erros.
    """
    # 1. Verificar Erros de Console/Rede (Já configurado no Contexto)
    
    # 2. Verificar Overlay de Erro do Next.js
    if await page.locator("nextjs-portal").count() > 0 or await page.locator("#__next-build-error-media").count() > 0:
        path = f"{SCREENSHOT_DIR}/crash_{route_name}.png"
        await page.screenshot(path=path)
        reporter.log_error(route_name, "Crash de Renderização (Next.js Overlay)", path)
        return

    # 3. Identificar Elementos Chave
    # Prioriza botões de ação primária (laranja) e navegação
    primary_buttons = page.locator("button.bg-orange-600, a.bg-orange-600")
    nav_links = page.locator("nav a")
    inputs = page.locator("input:not([type='hidden'])")

    # 4. Interagir com Inputs (Preenchimento Dummy - Read Only Check)
    count_inputs = await inputs.count()
    if count_inputs > 0:
        reporter.log_interaction(route_name, f"{count_inputs} Inputs Detectados", "INFO", "Campos de formulário presentes")

    # 5. Interagir com Botões (Apenas Hover/Check Visibility para evitar destruição)
    # Clicar aleatoriamente pode deletar dados. Vamos clicar apenas em abas ou modais seguros.
    # Para este teste "comprehensive", vamos focar em garantir que os elementos estão lá e são clicáveis.
    
    count_btns = await primary_buttons.count()
    for i in range(count_btns):
        btn = primary_buttons.nth(i)
        if await btn.is_visible():
            text = await btn.inner_text()
            if any(d in text for d in DANGEROUS_KEYWORDS):
                continue
            
            # Tenta hover para verificar interatividade
            try:
                await btn.hover(timeout=1000)
                reporter.log_interaction(route_name, text, "SUCCESS", "Elemento interativo (Hover OK)")
            except Exception as e:
                reporter.log_error(route_name, f"Falha ao interagir com {text}", None)

async def run_test():
    reporter = TestReporter()
    
    # Limpar diretórios de evidência
    if os.path.exists(SCREENSHOT_DIR): shutil.rmtree(SCREENSHOT_DIR)
    if os.path.exists(VIDEO_DIR): shutil.rmtree(VIDEO_DIR)
    os.makedirs(SCREENSHOT_DIR)
    os.makedirs(VIDEO_DIR)

    async with async_playwright() as p:
        # Browser com gravação de vídeo
        browser = await p.chromium.launch(headless=True) # Headless=True para CI, mas gera vídeo
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 800}
        )

        # Monitoramento Global
        context.on("console", lambda msg: reporter.log_error("CONSOLE", f"{msg.type}: {msg.text}") if msg.type == "error" else None)
        # Monitorar falhas de rede (API)
        context.on("response", lambda res: reporter.log_error("NETWORK", f"{res.status} {res.url}") if res.status >= 400 and "api" in res.url else None)

        page = await context.new_page()

        # 1. Autenticação
        print("🔑 Realizando Login Administrativo...")
        try:
            await page.goto(f"{BASE_URL}/admin/login")
            await page.fill('input[name="email"]', ADMIN_EMAIL)
            await page.fill('input[name="password"]', ADMIN_PASS)
            await page.click('button[type="submit"]')
            await page.wait_for_url("**/dashboard", timeout=15000)
            
            # GARANTIA: Injetar flag de tour completo imediatamente após login
            await page.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
            # Forçar recarregamento para aplicar o localStorage se necessário, ou confiar na injeção para as próximas navegações
            
            reporter.log_interaction("Login", "Formulário", "SUCCESS", "Autenticação realizada")
        except Exception as e:
            path = f"{SCREENSHOT_DIR}/login_fail.png"
            await page.screenshot(path=path)
            reporter.log_error("Login", f"Falha crítica: {str(e)}", path)
            await context.close()
            reporter.save_report()
            return

        # 2. Navegação e Exploração
        for route in ROUTES:
            if route.get("public"): continue # Pula rotas públicas no loop autenticado (testar separado se quiser)
            
            print(f"\n🔍 Auditando: {route['name']} ({route['url']})")
            try:
                # Navegar
                await page.goto(f"{BASE_URL}{route['url']}", wait_until="domcontentloaded")
                
                # Tratamento de Joyride (Tour) - Caso apareça
                await handle_onboarding_tour(page)
                
                # Esperar estabilização visual
                await page.wait_for_timeout(1000)
                
                # Screenshot da página
                screenshot_path = f"{SCREENSHOT_DIR}/{route['name']}.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                
                # Exploração
                await explore_page(page, route['name'], reporter)
                
                reporter.log_interaction(route['name'], "Carregamento", "SUCCESS", "Página renderizada")

            except Exception as e:
                path = f"{SCREENSHOT_DIR}/error_{route['name']}.png"
                await page.screenshot(path=path)
                reporter.log_error(route['name'], str(e), path)

        # 3. Finalização
        await context.close() # Salva o vídeo
        await browser.close()
        reporter.save_report()

if __name__ == "__main__":
    asyncio.run(run_test())
