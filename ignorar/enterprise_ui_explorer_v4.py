
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 12:00:00
import asyncio
import os
import json
import argparse
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator

# ==============================================================================
# 🧬 OPTIMUS v4.0 — BEHAVIORAL VALIDATION ENGINE
# ==============================================================================
# Diferenciais v4:
# 1. Modos: Inventory, Behavioral, Demo.
# 2. Login Real com Fallback.
# 3. Evidência Granular (Element Screenshots).
# 4. Storytelling em Vídeo.
# ==============================================================================

BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
OUTPUT_ROOT = Path("testesvisuais")
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
RUN_DIR = OUTPUT_ROOT / "fotos" / f"run_{RUN_ID}"
VIDEO_DIR = OUTPUT_ROOT / "videos" / f"run_{RUN_ID}"
PAGES_DIR = OUTPUT_ROOT / "paginas"

class EvidenceManager:
    def __init__(self, page_dir: Path):
        self.page_dir = page_dir
        self.imgs_dir = page_dir / "imgs"
        self.elements_dir = self.imgs_dir / "elements"
        self.elements_dir.mkdir(parents=True, exist_ok=True)

    async def capture_element(self, element_handle, name: str):
        try:
            clean_name = "".join(x for x in name if x.isalnum() or x in "_-")[:50]
            path = self.elements_dir / f"{clean_name}.png"
            await element_handle.screenshot(path=path)
            return str(path)
        except:
            return None

    async def capture_full_page(self, page: Page, suffix=""):
        path = self.imgs_dir / f"full_page{suffix}.png"
        await page.screenshot(path=path, full_page=True)
        return str(path)

class BehavioralEngine:
    def __init__(self, mode: str):
        self.mode = mode # inventory, behavioral, demo
        self.report_buffer = []
        self.setup_directories()

    def setup_directories(self):
        for d in [RUN_DIR, VIDEO_DIR, PAGES_DIR]:
            d.mkdir(parents=True, exist_ok=True)

    async def perform_real_login(self, page: Page):
        print("🔑 Tentando Login Real via UI...")
        try:
            await page.goto(f"{BASE_URL}/admin/login", wait_until="networkidle")
            
            # Preenche credenciais
            await page.fill('input[type="email"]', "admin@mesaflow.com")
            await page.fill('input[type="password"]', "123456")
            
            # Screenshot do estado preenchido
            await page.screenshot(path=RUN_DIR / "login_filled.png")
            
            # Submit
            await page.click('button[type="submit"]')
            
            # Validação
            try:
                await page.wait_for_url("**/dashboard", timeout=10000)
                print("   ✅ Login Real: SUCESSO")
                return True
            except:
                print("   ⚠️ Login Real: Timeout na navegação. Tentando fallback...")
                return False
        except Exception as e:
            print(f"   ❌ Login Real Falhou: {e}")
            return False

    async def inject_auth_token(self, context):
        print("💉 Injetando Token de Acesso (Fallback)...")
        await context.add_init_script("""
            localStorage.setItem('mesaflow_access_token', 'fake-jwt-token-for-testing');
            localStorage.setItem('mesaflow_user_role', 'owner');
            localStorage.setItem('mesaflow_tour_completed', 'true');
        """)

    async def run(self):
        print(f"🚀 Iniciando Optimus v4 (Mode: {self.mode.upper()})...")
        
        if not os.path.exists(ROUTES_FILE):
            print("❌ Erro: mapped_routes.json não encontrado.")
            return

        with open(ROUTES_FILE, "r", encoding="utf-8") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True) # Headless para CI
            
            context = await browser.new_context(
                record_video_dir=str(VIDEO_DIR),
                viewport={"width": 1280, "height": 720}
            )

            page = await context.new_page()

            # Estratégia de Login Híbrida
            login_success = await self.perform_real_login(page)
            if not login_success:
                await self.inject_auth_token(context)
                # Recarrega para aplicar token
                await page.goto(f"{BASE_URL}/admin/hamburgueria-ze/dashboard")

            for route in routes:
                await self.process_route(page, route)

            await context.close()
            await browser.close()
            self.save_master_report()

    async def process_route(self, page: Page, route_data: dict):
        url = f"{BASE_URL}{route_data['test_url']}"
        route_name = route_data['route_pattern'].replace("/", "_").strip("_") or "home"
        
        # Setup de Evidência
        page_output_dir = PAGES_DIR / route_name
        evidence = EvidenceManager(page_output_dir)
        
        print(f"\n🔭 Auditando: {url}")
        
        try:
            # Navegação
            response = await page.goto(url, wait_until="networkidle", timeout=15000)
            status = response.status if response else 0
            
            # Storytelling: Scroll Suave para Vídeo
            await self.smooth_scroll(page)
            
            # Captura Inicial
            await evidence.capture_full_page(page, "_before")

            # Inventário & Interação
            elements_report = await self.analyze_elements(page, evidence)
            
            # Registro
            self.report_buffer.append({
                "page": route_name,
                "url": url,
                "status": status,
                "elements": elements_report,
                "score": self.calculate_page_score(elements_report, status)
            })

            # Relatório da Página
            self.save_page_report(page_output_dir, route_name, elements_report, status)

        except Exception as e:
            print(f"   ❌ Falha Crítica em {url}: {e}")
            self.report_buffer.append({
                "page": route_name,
                "url": url,
                "status": "ERROR",
                "error": str(e),
                "score": 0
            })

    async def smooth_scroll(self, page: Page):
        # Simula leitura humana para o vídeo
        await page.evaluate("""
            async () => {
                await new Promise((resolve) => {
                    let totalHeight = 0;
                    let distance = 100;
                    let timer = setInterval(() => {
                        let scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        if(totalHeight >= scrollHeight){
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100);
                });
            }
        """)
        # Volta ao topo
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(500)

    async def analyze_elements(self, page: Page, evidence: EvidenceManager):
        selectors = ["button", "a[href]", "input:not([type='hidden'])", "[role='button']"]
        results = []
        
        # Coleta handles primeiro para evitar stale elements
        handles = await page.query_selector_all(", ".join(selectors))
        
        for i, handle in enumerate(handles):
            try:
                if not await handle.is_visible(): continue
                
                tag = await handle.evaluate("el => el.tagName.toLowerCase()")
                text = (await handle.inner_text()).strip()[:30].replace("\n", " ") or "Sem Texto"
                
                # Evidência Visual Individual
                img_path = await evidence.capture_element(handle, f"{tag}_{i}_{text}")
                
                interaction_result = "Skipped (Inventory Mode)"
                status = "NEUTRAL"

                # Modo Comportamental: Tenta Interagir (Hover/Focus)
                if self.mode in ['behavioral', 'demo']:
                    try:
                        await handle.hover(timeout=1000)
                        # Se for input, tenta digitar
                        if tag == "input":
                            await handle.fill("Test", timeout=1000)
                            interaction_result = "Input Fill OK"
                            status = "SUCCESS"
                        # Se for botão seguro (não delete), clica?
                        # Por segurança, no modo behavioral padrão, fazemos apenas hover/focus
                        # Para não destruir dados.
                        else:
                            interaction_result = "Hover OK"
                            status = "SUCCESS"
                    except Exception as e:
                        interaction_result = f"Interaction Failed: {str(e)[:50]}"
                        status = "FAIL"

                results.append({
                    "id": f"{tag}_{i}",
                    "type": tag,
                    "label": text,
                    "image": img_path,
                    "interaction": interaction_result,
                    "status": status
                })
                
            except:
                continue
                
        return results

    def calculate_page_score(self, elements, status):
        if status != 200: return 0
        if not elements: return 50 # Página vazia?
        
        failures = len([e for e in elements if e['status'] == 'FAIL'])
        total = len(elements)
        
        # Score base 100, penaliza falhas
        return max(0, 100 - (failures * 10))

    def save_page_report(self, output_dir: Path, name: str, elements: list, status: int):
        with open(output_dir / "docs" / "relatorio.md", "w", encoding="utf-8") as f:
            f.write(f"# 🕵️ Relatório Comportamental: {name}\n")
            f.write(f"**Status HTTP:** {status}\n\n")
            f.write("## 🧪 Matriz de Testes\n")
            f.write("| Elemento | Ação Esperada | Resultado | Status | Evidência |\n")
            f.write("|---|---|---|---|---|\n")
            for el in elements:
                icon = "✅" if el['status'] == "SUCCESS" else "⚠️" if el['status'] == "NEUTRAL" else "❌"
                img_link = f"[Ver]({el['image']})" if el['image'] else "-"
                f.write(f"| `{el['type']}` {el['label']} | Interação Básica | {el['interaction']} | {icon} | {img_link} |\n")

    def save_master_report(self):
        path = RUN_DIR / "todososbotoeseclicaveis.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write("# 📊 Inventário Global & Behavioral Score\n")
            f.write(f"**Run ID:** {RUN_ID} | **Mode:** {self.mode.upper()}\n\n")
            f.write("| Página | Status | Elementos | Score | Risco |\n")
            f.write("|---|---|---|---|---|\n")
            for item in self.report_buffer:
                score = item.get('score', 0)
                risk = "🟢 Baixo" if score > 90 else "🟡 Médio" if score > 70 else "🔴 Crítico"
                f.write(f"| {item['page']} | {item['status']} | {len(item.get('elements', []))} | {score}/100 | {risk} |\n")
        print(f"\n✅ Relatório Mestre gerado: {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["inventory", "behavioral", "demo"], default="behavioral")
    args = parser.parse_args()
    
    engine = BehavioralEngine(args.mode)
    asyncio.run(engine.run())

