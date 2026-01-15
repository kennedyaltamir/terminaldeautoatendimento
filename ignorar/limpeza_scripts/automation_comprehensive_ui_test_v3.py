# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 18:15:00
import asyncio
import os
import shutil
import requests
from datetime import datetime
from playwright.async_api import async_playwright, Page, BrowserContext

# ==============================================================================
# CONFIGURAÇÃO DO TESTE DE ESTRESSE DE UI (V3 - DEEP EXPLORATION)
# ==============================================================================
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

REPORT_FILE = "docs/reports/FULL_UI_TEST_REPORT_V3.md"
VIDEO_DIR = "docs/reports/videos"
SCREENSHOT_DIR = "docs/reports/evidence"

# Rotas Críticas para Auditoria
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

# Palavras-chave de segurança (Não clicar)
DANGEROUS_KEYWORDS = ["Sair", "Logout", "Excluir", "Remover", "Deletar", "Delete", "Limpar", "Desconectar"]

class TestReporter:
    def __init__(self):
        self.logs = []
        self.errors = []
        self.api_failures = []
        self.start_time = datetime.now()

    def log_interaction(self, page_name, action, result, details=""):
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "page": page_name,
            "action": action,
            "result": result,
            "details": details
        }
        self.logs.append(entry)
        icon = "✅" if result == "SUCCESS" else "⚠️"
        print(f"{icon} [{page_name}] {action}: {details}")

    def log_error(self, page_name, error_msg, screenshot_path=None):
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "page": page_name,
            "error": error_msg,
            "screenshot": screenshot_path
        }
        self.errors.append(entry)
        print(f"❌ [ERRO] {page_name}: {error_msg}")

    def log_api_failure(self, method, url, status):
        entry = f"{method} {url} -> {status}"
        if entry not in self.api_failures:
            self.api_failures.append(entry)
            print(f"🔥 [API FAIL] {entry}")

    def save_report(self):
        duration = datetime.now() - self.start_time
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Relatório de Teste de Interface V3 (Deep Exploration)\n")
            f.write(f"**Data:** {self.start_time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Duração:** {duration}\n")
            f.write(f"**Status API:** {'🔴 ERROS DETECTADOS' if self.api_failures else '🟢 ESTÁVEL'}\n\n")
            
            f.write("## 📹 Evidência em Vídeo\n")
            f.write("Os vídeos da execução foram salvos em `docs/reports/videos/`.\n\n")

            if self.api_failures:
                f.write("## 🔥 Falhas de API (Backend)\n")
                for fail in self.api_failures:
                    f.write(f"- `{fail}`\n")
                f.write("\n")

            if self.errors:
                f.write("## 🚨 Erros de Interface\n")
                for err in self.errors:
                    f.write(f"- **{err['page']}**: {err['error']}\n")
                    if err['screenshot']:
                        rel_path = os.path.relpath(err['screenshot'], os.path.dirname(REPORT_FILE))
                        f.write(f"  - Evidência: ![{err['page']}]({rel_path})\n")
                f.write("\n")
            
            f.write("## 📝 Log de Navegação\n")
            f.write("| Página | Ação | Resultado | Detalhes |\n")
            f.write("|---|---|---|---|\n")
            for log in self.logs:
                icon = "✅" if log['result'] == "SUCCESS" else "⚠️"
                f.write(f"| {log['page']} | `{log['action']}` | {icon} {log['result']} | {log['details']} |\n")
        
        print(f"\n📄 Relatório salvo em: {REPORT_FILE}")

async def kill_joyride(page: Page):
    """Remove agressivamente o tutorial do DOM."""
    await page.evaluate("""() => {
        const overlays = document.querySelectorAll('.react-joyride__overlay');
        overlays.forEach(el => el.remove());
        const portals = document.querySelectorAll('#react-joyride-portal');
        portals.forEach(el => el.remove());
        window.localStorage.setItem('mesaflow_tour_completed', 'true');
    }""")

async def check_backend_health():
    """Verifica se o backend está vivo antes de começar."""
    try:
        requests.get(f"{API_URL}/health", timeout=2)
        print("✅ Backend Online.")
        return True
    except:
        print("❌ Backend OFFLINE. O teste falhará.")
        return False

async def explore_page(page: Page, route_name: str, reporter: TestReporter):
    """
    Explora a página buscando interatividade real.
    """
    # 1. Kill Joyride
    await kill_joyride(page)
    
    # 2. Verificar Carregamento
    try:
        await page.wait_for_load_state("networkidle", timeout=5000)
    except:
        reporter.log_interaction(route_name, "Load", "WARN", "Network idle timeout (API lenta?)")

    # 3. Verificar se há dados (Tabelas/Listas)
    # Procura por elementos comuns de dados
    has_table = await page.locator("table").count() > 0
    has_cards = await page.locator(".grid > div").count() > 0
    
    if has_table:
        rows = await page.locator("table tbody tr").count()
        reporter.log_interaction(route_name, "Dados", "SUCCESS", f"Tabela encontrada com {rows} linhas")
    elif has_cards:
        cards = await page.locator(".grid > div").count()
        reporter.log_interaction(route_name, "Dados", "SUCCESS", f"Grid encontrado com {cards} cards")
    else:
        reporter.log_interaction(route_name, "Dados", "WARN", "Nenhum dado estruturado encontrado (Empty State?)")

    # 4. Interagir com Botões Seguros
    # Busca botões que não sejam perigosos
    buttons = await page.locator("button:visible, a.bg-orange-600:visible").all()
    
    interacted = 0
    for btn in buttons[:5]: # Limita a 5 interações por página
        try:
            text = await btn.inner_text()
            if not text: continue
            
            if any(d in text for d in DANGEROUS_KEYWORDS):
                continue

            # Hover para testar interatividade
            await btn.hover()
            # Se for um botão de "Novo" ou "Adicionar", tenta clicar e fechar modal
            if "Novo" in text or "Adicionar" in text or "Criar" in text:
                await btn.click()
                await page.wait_for_timeout(500)
                # Tenta fechar modal se abriu
                close_btn = page.locator("button svg.lucide-x").first
                if await close_btn.is_visible():
                    await close_btn.click()
                    reporter.log_interaction(route_name, f"Click '{text}'", "SUCCESS", "Modal abriu e fechou")
                else:
                    reporter.log_interaction(route_name, f"Click '{text}'", "SUCCESS", "Ação disparada")
                interacted += 1
        except:
            pass
    
    if interacted == 0:
        reporter.log_interaction(route_name, "Interação", "INFO", "Nenhum botão de ação primária clicado")

async def run_test():
    if not await check_backend_health():
        print("⚠️  Aviso: Backend offline. O teste de UI reportará erros de API.")

    reporter = TestReporter()
    
    # Limpar evidências
    if os.path.exists(SCREENSHOT_DIR): shutil.rmtree(SCREENSHOT_DIR)
    if os.path.exists(VIDEO_DIR): shutil.rmtree(VIDEO_DIR)
    os.makedirs(SCREENSHOT_DIR)
    os.makedirs(VIDEO_DIR)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 800},
            ignore_https_errors=True
        )

        # Monitoramento de Rede
        context.on("response", lambda res: reporter.log_api_failure(res.request.method, res.url, res.status) if res.status >= 400 and "api" in res.url else None)
        
        page = await context.new_page()

        # 1. Login (Crítico)
        print("🔑 Autenticando...")
        try:
            await page.goto(f"{BASE_URL}/admin/login")
            await page.fill('input[name="email"]', ADMIN_EMAIL)
            await page.fill('input[name="password"]', ADMIN_PASS)
            await page.click('button[type="submit"]')
            await page.wait_for_url("**/dashboard", timeout=15000)
            reporter.log_interaction("Login", "Auth", "SUCCESS", "Redirecionado para Dashboard")
        except Exception as e:
            path = f"{SCREENSHOT_DIR}/login_fatal.png"
            await page.screenshot(path=path)
            reporter.log_error("Login", f"Falha fatal: {e}", path)
            await context.close()
            reporter.save_report()
            return

        # 2. Loop de Rotas
        for route in ROUTES:
            if route['type'] == 'public': continue # Opcional: pular rotas públicas se já logado
            
            print(f"\n🔍 Auditando: {route['name']}")
            try:
                await page.goto(f"{BASE_URL}{route['url']}", wait_until="domcontentloaded")
                
                # Screenshot Inicial
                await page.screenshot(path=f"{SCREENSHOT_DIR}/{route['name']}_loaded.png")
                
                # Exploração
                await explore_page(page, route['name'], reporter)

            except Exception as e:
                path = f"{SCREENSHOT_DIR}/{route['name']}_crash.png"
                await page.screenshot(path=path)
                reporter.log_error(route['name'], str(e), path)

        await context.close()
        await browser.close()
        reporter.save_report()

if __name__ == "__main__":
    asyncio.run(run_test())
