import asyncio
import os
import json
import random
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext

# ==============================================================================
# CONFIGURAÇÃO ENTERPRISE V4 (HYPEROPTIMUS EDITION)
# ==============================================================================
BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
AUTH_STATE = "auth_state.json"

# Estrutura de Pastas de Evidência
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
BASE_EVIDENCE_DIR = Path(f"testesvisuais/run_{RUN_ID}")
IMG_DIR = BASE_EVIDENCE_DIR / "fotos"
VID_DIR = BASE_EVIDENCE_DIR / "videos"
REPORT_MD = IMG_DIR / "ultimate_report_v4.md"

# Configuração de Velocidade Humana
MIN_DELAY = 500  # ms
MAX_DELAY = 1500 # ms

class EnterpriseExplorerV4:
    def __init__(self):
        self.results = []
        self.setup_dirs()

    def setup_dirs(self):
        if not IMG_DIR.exists(): os.makedirs(IMG_DIR)
        if not VID_DIR.exists(): os.makedirs(VID_DIR)

    async def human_delay(self, page: Page):
        """Simula o tempo de pensamento de um usuário humano."""
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        await page.wait_for_timeout(delay)

    async def safe_hover(self, element):
        """Tenta fazer hover com scroll forçado e fallback."""
        try:
            await element.scroll_into_view_if_needed(timeout=1000)
            await element.hover(timeout=1000, force=True)
            return True
        except:
            try:
                await element.evaluate("el => el.scrollIntoView({block: 'center', inline: 'center'})")
                await element.hover(timeout=1000, force=True)
                return True
            except:
                return False

    async def capture_page_audit(self, route_info: dict):
        """
        Executa a auditoria isolada de uma página em um novo contexto.
        Gera vídeo único e screenshots detalhados.
        """
        url = f"{BASE_URL}{route_info['test_url']}"
        safe_name = route_info['route_pattern'].replace("/", "_").strip("_") or "home"
        print(f"\n🎬 Iniciando Auditoria V4: {url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Contexto Isolado para Vídeo Único
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                record_video_dir=VID_DIR,
                record_video_size={"width": 1280, "height": 800},
                storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None
            )
            
            # Injeção de Scripts Anti-Ruído
            await context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
            
            page = await context.new_page()
            
            # Captura de Erros de Console
            page_errors = []
            page.on("console", lambda msg: page_errors.append(f"[CONSOLE] {msg.type}: {msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda exc: page_errors.append(f"[CRASH] {exc}"))

            try:
                # Navegação Lenta
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await self.human_delay(page)

                # Limpeza de Modais
                await page.evaluate("""() => {
                    document.querySelectorAll('.react-joyride__overlay').forEach(el => el.remove());
                    document.querySelectorAll('#react-joyride-portal').forEach(el => el.remove());
                }""")

                # Screenshot Inicial
                await page.screenshot(path=f"{IMG_DIR}/{safe_name}_00_load.png", full_page=True)

                # Detecção de Elementos (Estratégia Ampliada)
                selectors = [
                    "button:visible", 
                    "a[href]:visible", 
                    "input[type='submit']:visible", 
                    "[role='button']:visible",
                    "div[onClick]:visible" # React clickable divs
                ]
                handles = await page.query_selector_all(", ".join(selectors))
                
                print(f"   👁️  {len(handles)} elementos interativos detectados.")

                if len(handles) == 0:
                    # Diagnóstico de Empty State
                    body_text = await page.inner_text("body")
                    status = "EMPTY_STATE"
                    if "Error" in body_text or "404" in body_text:
                        status = "ERROR_PAGE"
                    
                    self.results.append({
                        "page": route_info['route_pattern'],
                        "url": url,
                        "element": "NENHUM",
                        "status": status,
                        "logs": page_errors
                    })
                
                # Interação Lenta (Amostragem de 5 elementos para não gerar vídeos de 1 hora)
                for i, handle in enumerate(handles[:5]):
                    try:
                        if not await handle.is_visible(): continue
                        
                        # Identificação
                        text = (await handle.inner_text()).strip() or "Icon/Unlabeled"
                        tag = await handle.evaluate("el => el.tagName.toLowerCase()")
                        
                        # Hover (Ação 1)
                        await self.safe_hover(handle)
                        await self.human_delay(page) # Pausa para vídeo capturar o hover state
                        
                        # Highlight
                        await handle.evaluate("el => el.style.border = '3px solid #ea580c'") # Laranja MesaFlow
                        await page.screenshot(path=f"{IMG_DIR}/{safe_name}_el_{i}.png")
                        await handle.evaluate("el => el.style.border = ''")

                        self.results.append({
                            "page": route_info['route_pattern'],
                            "url": url,
                            "element": f"{tag}: {text}",
                            "status": "VERIFIED",
                            "logs": page_errors
                        })

                    except Exception as e:
                        print(f"   ⚠️  Erro ao interagir com elemento {i}: {e}")

            except Exception as e:
                print(f"   ❌ Falha crítica na página: {e}")
                self.results.append({
                    "page": route_info['route_pattern'],
                    "url": url,
                    "element": "CRASH",
                    "status": "CRASH",
                    "logs": page_errors + [str(e)]
                })
            
            finally:
                # Garante fechamento para salvar vídeo
                await context.close()
                
                # Renomear vídeo (Playwright gera nome aleatório)
                # FIX: page.video é uma propriedade, não um método.
                try:
                    video = page.video
                    if video:
                        video_path = await video.path()
                        if video_path:
                            new_video_name = f"{safe_name}.webm"
                            # Pequeno delay para garantir liberação do arquivo
                            await asyncio.sleep(0.5)
                            try:
                                os.rename(video_path, VID_DIR / new_video_name)
                                print(f"   📹 Vídeo salvo: {new_video_name}")
                            except Exception as rename_err:
                                print(f"   ⚠️  Erro ao renomear vídeo: {rename_err}")
                except Exception as video_err:
                    print(f"   ⚠️  Erro ao processar vídeo: {video_err}")

    def generate_report(self):
        print(f"\n📝 Gerando Relatório Ultimate V4 em {REPORT_MD}...")
        with open(REPORT_MD, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Relatório Ultimate UI V4 (Run {RUN_ID})\n\n")
            f.write("## 📂 Artefatos\n")
            f.write(f"- **Vídeos:** `{VID_DIR}` (Um por página)\n")
            f.write(f"- **Screenshots:** `{IMG_DIR}`\n\n")
            f.write("## 📊 Matriz de Auditoria\n")
            f.write("| Página | Elemento | Status | Logs Críticos |\n")
            f.write("|---|---|---|---|\n")
            
            for item in self.results:
                status_icon = "🟢"
                if item['status'] == "EMPTY_STATE": status_icon = "🟡"
                if item['status'] == "ERROR_PAGE": status_icon = "🟠"
                if item['status'] == "CRASH": status_icon = "🔴"
                
                logs = "<br>".join(item['logs']) if item['logs'] else "-"
                f.write(f"| `{item['page']}` | {item['element']} | {status_icon} {item['status']} | {logs} |\n")

    async def run_all(self):
        if not os.path.exists(ROUTES_FILE):
            print("❌ Arquivo de rotas não encontrado. Execute map_routes.py primeiro.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        # Login Inicial (Se necessário)
        if not os.path.exists(AUTH_STATE):
            print("🔑 Gerando estado de autenticação...")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard", timeout=15000)
                await page.context.storage_state(path=AUTH_STATE)
                await browser.close()

        # Execução Sequencial (Para não sobrecarregar e garantir vídeos limpos)
        for route in routes:
            await self.capture_page_audit(route)
        
        self.generate_report()

if __name__ == "__main__":
    explorer = EnterpriseExplorerV4()
    asyncio.run(explorer.run_all())
