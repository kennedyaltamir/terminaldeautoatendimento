# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 18:55:00
import asyncio
import os
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# ==============================================================================
# CONFIGURAÇÃO ENTERPRISE
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

class EnterpriseExplorer:
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
            # Inicia gravação de vídeo para esta página (contexto isolado seria ideal, mas vamos usar global)
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500) # Estabilização visual

            # Screenshot da Página Inteira
            safe_name = route_info['route_pattern'].replace("/", "_").strip("_") or "home"
            await page.screenshot(path=f"{IMG_DIR}/{safe_name}_full.png", full_page=True)

            # Detectar Elementos Clicáveis
            # Seleciona botões, links e inputs submit visíveis
            elements = await page.locator("button:visible, a[href]:visible, input[type='submit']:visible, [role='button']:visible").all()
            
            print(f"   🧩 {len(elements)} elementos interativos detectados.")

            for i, el in enumerate(elements):
                try:
                    text = (await el.inner_text()).strip() or (await el.get_attribute("aria-label")) or "Icon/Unlabeled"
                    tag = await el.evaluate("el => el.tagName.toLowerCase()")
                    
                    # Inferir comportamento
                    expected = infer_expected_behavior(text, tag)
                    
                    # Tentar interagir (Hover apenas para não destruir dados no teste de mapeamento)
                    # Para um teste destrutivo real, usaríamos click, mas aqui é mapeamento.
                    await el.hover()
                    
                    # Screenshot do Elemento (Highlight)
                    box = await el.bounding_box()
                    if box:
                        # Desenha borda vermelha para evidência
                        await el.evaluate("el => el.style.border = '3px solid red'")
                        await page.screenshot(path=f"{IMG_DIR}/{safe_name}_el_{i}.png")
                        await el.evaluate("el => el.style.border = ''") # Limpa

                    self.results.append({
                        "page": route_info['route_pattern'],
                        "url": url,
                        "element_text": text,
                        "element_tag": tag,
                        "expected_behavior": expected,
                        "status": "DETECTED",
                        "screenshot": f"{safe_name}_el_{i}.png"
                    })

                except Exception as e:
                    print(f"   ⚠️  Erro ao analisar elemento {i}: {e}")

        except Exception as e:
            print(f"   ❌ Erro crítico na página {url}: {e}")
            await page.screenshot(path=f"{IMG_DIR}/ERROR_{safe_name}.png")

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
                f.write(f"| `{item['page']}` | **{item['element_text']}** | `{item['element_tag']}` | {item['expected_behavior']} | 🟢 {item['status']} | [Ver Foto]({item['screenshot']}) |\n")

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
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard")
                await context.storage_state(path=AUTH_STATE)

            # Iterar Rotas
            for route in routes:
                await self.analyze_page(page, route)

            await context.close()
            await browser.close()
            
            self.generate_markdown_report()

if __name__ == "__main__":
    explorer = EnterpriseExplorer()
    asyncio.run(explorer.run())
