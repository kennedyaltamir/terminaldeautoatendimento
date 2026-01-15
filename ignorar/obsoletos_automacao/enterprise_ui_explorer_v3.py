# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 19:45:00
import asyncio
import os
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# ==============================================================================
# CONFIGURAÇÃO ENTERPRISE V3 (RESILIENT & DIAGNOSTIC)
# ==============================================================================
BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
AUTH_STATE = "auth_state.json"

# Estrutura de Pastas de Evidência
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
BASE_EVIDENCE_DIR = Path(f"testesvisuais/run_{RUN_ID}")
IMG_DIR = BASE_EVIDENCE_DIR / "fotos"
VID_DIR = BASE_EVIDENCE_DIR / "videos"
REPORT_MD = IMG_DIR / "todososbotoeseclicaveis.md"

def infer_expected_behavior(element_text, element_tag):
    text = element_text.lower()
    if "salvar" in text or "entrar" in text or "enviar" in text: return "Submissão de Formulário"
    if "excluir" in text or "remover" in text: return "Ação Destrutiva (Modal)"
    if "voltar" in text or "cancelar" in text: return "Navegação/Fechamento"
    if "adicionar" in text or "novo" in text: return "Abertura de Modal/Form"
    return "Interação de UI"

class EnterpriseExplorerV3:
    def __init__(self):
        self.results = []
        self.console_logs = []
        self.setup_dirs()

    def setup_dirs(self):
        if not IMG_DIR.exists(): os.makedirs(IMG_DIR)
        if not VID_DIR.exists(): os.makedirs(VID_DIR)

    def log_console(self, msg):
        if msg.type == "error":
            self.console_logs.append(f"[{msg.type}] {msg.text}")

    async def safe_hover(self, element):
        """Tenta fazer hover com scroll forçado e fallback."""
        try:
            # Tenta scroll nativo do Playwright
            await element.scroll_into_view_if_needed(timeout=1000)
            await element.hover(timeout=1000, force=True)
            return True
        except:
            try:
                # Fallback: Scroll via JS
                await element.evaluate("el => el.scrollIntoView({block: 'center', inline: 'center'})")
                await element.hover(timeout=1000, force=True)
                return True
            except:
                return False

    async def analyze_page(self, page: Page, route_info: dict):
        url = f"{BASE_URL}{route_info['test_url']}"
        print(f"\n🕵️  Analisando: {url}")
        self.console_logs = [] # Limpa logs da página anterior
        
        # Listener de Console para Diagnóstico
        page.on("console", self.log_console)

        try:
            # Tentativa de Navegação com Retry
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            except Exception as nav_err:
                print(f"   ⚠️  Falha inicial de navegação. Tentando novamente... ({nav_err})")
                await page.wait_for_timeout(2000)
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)

            # Kill Joyride & Modais Bloqueantes
            await page.evaluate("""() => {
                document.querySelectorAll('.react-joyride__overlay').forEach(el => el.remove());
                document.querySelectorAll('#react-joyride-portal').forEach(el => el.remove());
            }""")

            # Screenshot Full Page
            safe_name = route_info['route_pattern'].replace("/", "_").strip("_") or "home"
            await page.screenshot(path=f"{IMG_DIR}/{safe_name}_full.png", full_page=True)

            # Detectar Elementos
            handles = await page.query_selector_all("button:visible, a[href]:visible, input[type='submit']:visible, [role='button']:visible")
            
            print(f"   🧩 {len(handles)} elementos interativos detectados.")

            if len(handles) == 0:
                self.results.append({
                    "page": route_info['route_pattern'],
                    "url": url,
                    "element_text": "NENHUM",
                    "element_tag": "-",
                    "expected_behavior": "-",
                    "status": "EMPTY_STATE",
                    "screenshot": None,
                    "logs": self.console_logs
                })

            # Analisar primeiros 15 elementos
            for i, handle in enumerate(handles[:15]):
                try:
                    if not await handle.is_visible(): continue

                    text = (await handle.inner_text()).strip() or "Icon/Unlabeled"
                    tag = await handle.evaluate("el => el.tagName.toLowerCase()")
                    expected = infer_expected_behavior(text, tag)
                    
                    # Interação Segura
                    hovered = await self.safe_hover(handle)
                    
                    status = "DETECTED" if hovered else "UNREACHABLE"
                    screenshot_path = None

                    if hovered:
                        # Highlight e Screenshot
                        box = await handle.bounding_box()
                        if box:
                            await handle.evaluate("el => el.style.border = '3px solid red'")
                            screenshot_path = f"{safe_name}_el_{i}.png"
                            await page.screenshot(path=f"{IMG_DIR}/{screenshot_path}")
                            await handle.evaluate("el => el.style.border = ''")

                    self.results.append({
                        "page": route_info['route_pattern'],
                        "url": url,
                        "element_text": text,
                        "element_tag": tag,
                        "expected_behavior": expected,
                        "status": status,
                        "screenshot": screenshot_path,
                        "logs": [] # Logs são globais da página, não por elemento
                    })

                except Exception as e:
                    print(f"   ⚠️  Erro no elemento {i}: {e}")

        except Exception as e:
            print(f"   ❌ Erro crítico na página {url}: {e}")
            # Se houver logs de console capturados, exibe-os
            if self.console_logs:
                print("   📜 Logs do Navegador capturados:")
                for log in self.console_logs:
                    print(f"      {log}")
            
            self.results.append({
                "page": route_info['route_pattern'],
                "url": url,
                "element_text": "CRASH",
                "element_tag": "-",
                "expected_behavior": "-",
                "status": "CRASH",
                "screenshot": None,
                "logs": self.console_logs
            })
        finally:
            page.remove_listener("console", self.log_console)

    def generate_markdown_report(self):
        print(f"\n📝 Gerando Relatório Enterprise em {REPORT_MD}...")
        with open(REPORT_MD, "w", encoding="utf-8") as f:
            f.write(f"# 📊 Relatório de Mapeamento de Interface (Run {RUN_ID})\n\n")
            f.write("## 📹 Evidências\n")
            f.write(f"- **Vídeos:** `{VID_DIR}`\n")
            f.write(f"- **Screenshots:** `{IMG_DIR}`\n\n")

            f.write("## 🖱️ Matriz de Interatividade\n")
            f.write("| Página | Elemento | Tipo | Comportamento Esperado | Status | Evidência | Logs |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            
            for item in self.results:
                evidence_link = f"[Ver Foto]({item['screenshot']})" if item['screenshot'] else "-"
                
                status_icon = "🟢"
                if item['status'] == "UNREACHABLE": status_icon = "🟠"
                if item['status'] == "EMPTY_STATE": status_icon = "🟡"
                if item['status'] == "CRASH": status_icon = "🔴"
                
                logs_md = "<br>".join(item['logs']) if item['logs'] else "-"
                
                f.write(f"| `{item['page']}` | **{item['element_text']}** | `{item['element_tag']}` | {item['expected_behavior']} | {status_icon} {item['status']} | {evidence_link} | {logs_md} |\n")

    async def run(self):
        if not os.path.exists(ROUTES_FILE):
            print("❌ Arquivo de rotas não encontrado.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                record_video_dir=VID_DIR,
                record_video_size={"width": 1280, "height": 800},
                storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None
            )
            await context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
            page = await context.new_page()

            # Login se necessário
            if not os.path.exists(AUTH_STATE):
                print("🔑 Realizando Login Inicial...")
                try:
                    await page.goto(f"{BASE_URL}/admin/login")
                    await page.fill('input[name="email"]', "admin@mesaflow.com")
                    await page.fill('input[name="password"]', "123456")
                    await page.click('button[type="submit"]')
                    await page.wait_for_url("**/dashboard", timeout=15000)
                    await context.storage_state(path=AUTH_STATE)
                except Exception as e:
                    print(f"❌ Falha no login: {e}")
                    return

            for route in routes:
                await self.analyze_page(page, route)

            await context.close()
            await browser.close()
            self.generate_markdown_report()

if __name__ == "__main__":
    explorer = EnterpriseExplorerV3()
    asyncio.run(explorer.run())
