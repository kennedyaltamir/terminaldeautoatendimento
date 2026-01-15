# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 19:20:00
import asyncio
import os
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# ==============================================================================
# CONFIGURAÇÃO ENTERPRISE V2 (ROBUST & FAST)
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

# Heurística de Comportamento Esperado
def infer_expected_behavior(element_text, element_tag):
    text = element_text.lower()
    if "salvar" in text or "entrar" in text or "enviar" in text:
        return "Submissão de Formulário / Redirecionamento"
    if "excluir" in text or "remover" in text:
        return "Modal de Confirmação / Toast de Sucesso"
    if "voltar" in text or "cancelar" in text:
        return "Navegação para trás / Fechamento de Modal"
    if "adicionar" in text or "novo" in text:
        return "Abertura de Modal ou Nova Página"
    return "Navegação ou Interação de UI"

class EnterpriseExplorerV2:
    def __init__(self):
        self.results = []
        self.setup_dirs()

    def setup_dirs(self):
        if not IMG_DIR.exists(): os.makedirs(IMG_DIR)
        if not VID_DIR.exists(): os.makedirs(VID_DIR)

    async def analyze_page(self, page: Page, route_info: dict):
        url = f"{BASE_URL}{route_info['test_url']}"
        print(f"\n🕵️  Analisando: {url}")
        
        try:
            # Timeout reduzido para falhar rápido se a página travar
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            
            # Kill Joyride (Overlay que bloqueia cliques)
            await page.evaluate("""() => {
                const overlays = document.querySelectorAll('.react-joyride__overlay');
                overlays.forEach(el => el.remove());
                const portals = document.querySelectorAll('#react-joyride-portal');
                portals.forEach(el => el.remove());
            }""")

            # Screenshot da Página Inteira
            safe_name = route_info['route_pattern'].replace("/", "_").strip("_") or "home"
            await page.screenshot(path=f"{IMG_DIR}/{safe_name}_full.png", full_page=True)

            # Detectar Elementos Clicáveis (Limitado a 10 para não travar em loops infinitos)
            # Usamos ElementHandles para evitar re-query e timeouts
            handles = await page.query_selector_all("button:visible, a[href]:visible, input[type='submit']:visible, [role='button']:visible")
            
            print(f"   🧩 {len(handles)} elementos interativos detectados.")

            for i, handle in enumerate(handles[:10]):
                try:
                    # Verifica se o elemento ainda está conectado ao DOM
                    if not await handle.is_visible(): continue

                    text = (await handle.inner_text()).strip() or "Icon/Unlabeled"
                    tag = await handle.evaluate("el => el.tagName.toLowerCase()")
                    
                    # Inferir comportamento
                    expected = infer_expected_behavior(text, tag)
                    
                    # Tentar interagir (Hover com timeout curto)
                    try:
                        await handle.hover(timeout=2000)
                        
                        # Screenshot do Elemento (Highlight)
                        box = await handle.bounding_box()
                        if box:
                            await handle.evaluate("el => el.style.border = '3px solid red'")
                            await page.screenshot(path=f"{IMG_DIR}/{safe_name}_el_{i}.png")
                            await handle.evaluate("el => el.style.border = ''") # Limpa

                        self.results.append({
                            "page": route_info['route_pattern'],
                            "url": url,
                            "element_text": text,
                            "element_tag": tag,
                            "expected_behavior": expected,
                            "status": "DETECTED",
                            "screenshot": f"{safe_name}_el_{i}.png"
                        })
                    except Exception as hover_err:
                        print(f"   ⚠️  Timeout no hover do elemento {i}: {hover_err}")
                        # Se falhar o hover, registra como detectado mas com aviso
                        self.results.append({
                            "page": route_info['route_pattern'],
                            "url": url,
                            "element_text": text,
                            "element_tag": tag,
                            "expected_behavior": expected,
                            "status": "WARN_TIMEOUT",
                            "screenshot": None
                        })

                except Exception as e:
                    print(f"   ⚠️  Erro ao analisar elemento {i}: {e}")

        except Exception as e:
            print(f"   ❌ Erro crítico na página {url}: {e}")
            # Tenta tirar print do erro se a página carregou parcialmente
            try:
                await page.screenshot(path=f"{IMG_DIR}/ERROR_{safe_name}.png")
            except: pass

    def generate_markdown_report(self):
        print(f"\n📝 Gerando Relatório Enterprise em {REPORT_MD}...")
        with open(REPORT_MD, "w", encoding="utf-8") as f:
            f.write(f"# 📊 Relatório de Mapeamento de Interface (Run {RUN_ID})\n\n")
            f.write("Este documento lista todos os pontos de interação detectados automaticamente pelo robô explorador.\n\n")
            
            f.write("## 📹 Evidências de Vídeo\n")
            f.write(f"Os vídeos de navegação estão disponíveis em: `{VID_DIR}`\n\n")

            f.write("## 🖱️ Matriz de Interatividade\n")
            f.write("| Página | Elemento | Tipo | Comportamento Esperado | Status | Evidência |\n")
            f.write("|---|---|---|---|---|---|\n")
            
            for item in self.results:
                evidence_link = f"[Ver Foto]({os.path.basename(item['screenshot'])})" if item['screenshot'] else "-"
                icon = "🟢" if item['status'] == "DETECTED" else "🟡"
                f.write(f"| `{item['page']}` | **{item['element_text']}** | `{item['element_tag']}` | {item['expected_behavior']} | {icon} {item['status']} | {evidence_link} |\n")

    async def run(self):
        # Carregar rotas
        if not os.path.exists(ROUTES_FILE):
            print("❌ Arquivo de rotas não encontrado. Rode map_routes.py primeiro.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Contexto com Vídeo e Auth
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                record_video_dir=VID_DIR,
                record_video_size={"width": 1280, "height": 800},
                storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None
            )
            
            # Injeção de Scripts Anti-Bloqueio
            await context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")

            page = await context.new_page()

            # Se não tiver auth state, faz login primeiro
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

            # Iterar Rotas
            for route in routes:
                await self.analyze_page(page, route)

            await context.close()
            await browser.close()
            
            self.generate_markdown_report()

if __name__ == "__main__":
    explorer = EnterpriseExplorerV2()
    asyncio.run(explorer.run())
