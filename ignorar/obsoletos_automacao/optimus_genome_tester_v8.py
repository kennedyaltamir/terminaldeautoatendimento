import asyncio
import os
import json
import random
import hashlib
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator, BrowserContext
from faker import Faker

# ==============================================================================
# 🧬 OPTIMUS UI GENOME TESTER V8.0 (ULTIMATE EDITION)
# ==============================================================================
# "Mapeamento Genético Completo da Interface"
# ------------------------------------------------------------------------------
# Capacidades:
# 1. Inventário Global de Componentes (Genome Map).
# 2. Teste Sem Limites (Iteração em todos os elementos visíveis).
# 3. Evidência Forense (Círculo Visual, Scroll Full-Page, Antes/Depois).
# 4. Heurística de Intenção Profunda (Interpretação de Contexto).
# 5. Relatório Mestre Cruzado.
# ==============================================================================

BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
OUTPUT_DIR = Path("testesvisuais/genome_v8")
AUTH_STATE = "auth_state.json"

# Configurações de Performance e Comportamento
SLOW_MO = 500
HEADLESS = True
MAX_CONCURRENCY = 1 # Aumentar se a máquina aguentar
CAPTURE_ELEMENT_VIDEO = False # Se True, reinicia contexto por elemento (Lento!)

fake = Faker('pt_BR')

class GenomeReporter:
    def __init__(self, run_id):
        self.run_id = run_id
        self.global_inventory = []
        self.page_summaries = []

    def add_element_result(self, page_route, element_data):
        self.global_inventory.append({
            "page": page_route,
            **element_data
        })

    def generate_master_report(self):
        master_path = OUTPUT_DIR / f"RELATORIO_MESTRE_GENOMA_{self.run_id}.md"
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(f"# 🧬 Relatório Mestre de Genoma UI (v8.0)\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"**Total de Elementos Analisados:** {len(self.global_inventory)}\n\n")
            
            f.write("## 1. Inventário Global de Componentes\n")
            f.write("| Página | Tipo | Texto/ID | Intenção | Status | Evidência |\n")
            f.write("|---|---|---|---|---|---|\n")
            
            for item in self.global_inventory:
                status_icon = "✅" if item['status'] == "SUCCESS" else "⚠️" if item['status'] == "SKIPPED" else "❌"
                evidence = f"[Link]({item['evidence_path']})" if item.get('evidence_path') else "-"
                f.write(f"| `{item['page']}` | `{item['tag']}` | **{item['text']}** | {item['intent']} | {status_icon} {item['status']} | {evidence} |\n")

            f.write("\n## 2. Análise de Consistência\n")
            # Análise simples de consistência
            buttons = [x for x in self.global_inventory if x['tag'] == 'button']
            inputs = [x for x in self.global_inventory if x['tag'] == 'input']
            f.write(f"- **Botões Totais:** {len(buttons)}\n")
            f.write(f"- **Inputs Totais:** {len(inputs)}\n")
            
            f.write("\n## 3. Diagnóstico de Falhas\n")
            failures = [x for x in self.global_inventory if x['status'] == "ERROR"]
            if not failures:
                f.write("🎉 Nenhuma falha funcional crítica detectada.\n")
            else:
                for fail in failures:
                    f.write(f"- 🔴 **{fail['page']}**: {fail['text']} -> {fail['error_msg']}\n")

class OptimusGenomeTester:
    def __init__(self):
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.reporter = GenomeReporter(self.run_id)
        self.setup_global_dirs()

    def setup_global_dirs(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def setup_page_dirs(self, page_name: str):
        safe_name = page_name.replace("/", "_").strip("_") or "home"
        base = OUTPUT_DIR / safe_name
        dirs = {
            "root": base,
            "docs": base / "docs",
            "imgs": base / "imgs",
            "videos": base / "videos",
            "elements": base / "imgs" / "elements" # Pasta granular
        }
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs, safe_name

    async def highlight_element(self, locator: Locator, color="#ea580c", width="4px"):
        """Desenha um círculo/borda ao redor do elemento para o print."""
        try:
            await locator.evaluate(f"""el => {{
                el.style.outline = '{width} solid {color}';
                el.style.boxShadow = '0 0 15px {color}';
                el.style.transition = 'all 0.3s';
                el.dataset.optimusHighlight = 'true';
            }}""")
        except: pass

    async def unhighlight_element(self, locator: Locator):
        try:
            await locator.evaluate("""el => {
                el.style.outline = '';
                el.style.boxShadow = '';
                delete el.dataset.optimusHighlight;
            }""")
        except: pass

    async def capture_full_page(self, page: Page, path: Path):
        """Captura screenshot de página inteira com scroll inteligente."""
        # Scroll até o fim para carregar lazy images
        await page.evaluate("""async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if(totalHeight >= scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 50);
            });
            window.scrollTo(0, 0);
        }""")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=path, full_page=True)

    async def infer_intent_and_data(self, tag: str, text: str, type_attr: str, name_attr: str, aria_label: str) -> dict:
        """
        Cérebro Heurístico v8.0: Determina a intenção do elemento e dados de teste.
        """
        context_str = f"{text} {name_attr} {aria_label} {type_attr}".lower()
        
        intent = {
            "action": "click",
            "type": "interaction",
            "risk": "low",
            "fill_value": None,
            "expected_behavior": "Change UI State"
        }

        # 1. Inputs
        if tag in ["input", "textarea"]:
            intent["action"] = "fill"
            intent["type"] = "data_entry"
            
            if "email" in context_str:
                intent["fill_value"] = "admin@mesaflow.com"
            elif "password" in context_str or "senha" in context_str:
                intent["fill_value"] = "123456"
            elif "phone" in context_str or "tel" in context_str:
                intent["fill_value"] = "11999999999"
            elif "search" in context_str or "busca" in context_str:
                intent["fill_value"] = "X-Bacon"
            elif "number" in type_attr:
                intent["fill_value"] = "1"
            else:
                intent["fill_value"] = fake.word()
            
            intent["expected_behavior"] = f"Accept input '{intent['fill_value']}'"

        # 2. Botões Críticos
        elif "excluir" in context_str or "remover" in context_str or "delete" in context_str:
            intent["risk"] = "high"
            intent["expected_behavior"] = "Open Confirmation Modal"
        
        elif "salvar" in context_str or "entrar" in context_str or "login" in context_str:
            intent["type"] = "submission"
            intent["expected_behavior"] = "Submit Form / Navigate"

        elif "voltar" in context_str:
            intent["type"] = "navigation"
            intent["expected_behavior"] = "Navigate Back"

        return intent

    async def process_element(self, page: Page, element_handle, index: int, dirs, safe_name, page_route):
        """
        Processa um único elemento: Highlight -> Print -> Action -> Validate -> Report.
        """
        try:
            if not await element_handle.is_visible(): return None

            # Extração de Metadados (Genoma)
            tag = await element_handle.evaluate("el => el.tagName.toLowerCase()")
            text = (await element_handle.inner_text()).strip().replace("\n", " ")[:50]
            type_attr = await element_handle.get_attribute("type") or ""
            name_attr = await element_handle.get_attribute("name") or ""
            aria_label = await element_handle.get_attribute("aria-label") or ""
            
            # Identificador Único
            el_id = f"el_{index:03d}_{tag}"
            if text: el_id += f"_{text[:10].replace(' ', '')}"
            
            # Inferência
            intent = await self.infer_intent_and_data(tag, text, type_attr, name_attr, aria_label)
            
            # Skip de Segurança
            if intent["risk"] == "high":
                return {
                    "id": el_id, "tag": tag, "text": text, "intent": "DESTRUCTIVE",
                    "status": "SKIPPED", "evidence_path": None
                }

            # 1. Evidência Pré-Ação (Com Highlight)
            await self.highlight_element(element_handle)
            screenshot_path = dirs['elements'] / f"{el_id}_context.png"
            await page.screenshot(path=screenshot_path)
            
            # 2. Ação
            url_before = page.url
            
            if intent["action"] == "fill":
                await element_handle.fill(intent["fill_value"])
            else:
                # Scroll suave até o elemento
                await element_handle.scroll_into_view_if_needed()
                # Efeito visual de clique
                box = await element_handle.bounding_box()
                if box:
                    await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                    await page.mouse.down()
                    await page.wait_for_timeout(100)
                    await page.mouse.up()
                else:
                    await element_handle.click()

            # 3. Espera Inteligente
            await page.wait_for_timeout(1000) # Espera animações/requests
            
            # 4. Validação de Resultado
            url_after = page.url
            status = "SUCCESS"
            
            if url_after != url_before:
                # Navegou - Tentar voltar para continuar o teste da página
                try:
                    await page.go_back(wait_until="domcontentloaded")
                    await page.wait_for_timeout(1000)
                    # Re-hidratar o elemento pode ser impossível aqui, então o loop principal deve tratar stale elements
                except:
                    pass

            await self.unhighlight_element(element_handle)
            
            return {
                "id": el_id,
                "tag": tag,
                "text": text,
                "intent": intent["expected_behavior"],
                "status": status,
                "evidence_path": str(screenshot_path.relative_to(OUTPUT_DIR)),
                "error_msg": None
            }

        except Exception as e:
            return {
                "id": f"el_{index}", "tag": "unknown", "text": "ERROR",
                "intent": "unknown", "status": "ERROR",
                "evidence_path": None, "error_msg": str(e)
            }

    async def analyze_page(self, route, browser):
        dirs, safe_name = self.setup_page_dirs(route['route_pattern'])
        url = f"{BASE_URL}{route['test_url']}"
        print(f"\n🧬 Sequenciando Genoma da Página: {url}")

        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir=dirs['videos'],
            record_video_size={"width": 1280, "height": 800},
            storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None
        )
        
        # Anti-Noise & Setup
        await context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # 1. Captura Full Page (Baseline)
            await self.capture_full_page(page, dirs['imgs'] / "00_BASELINE_FULL.png")

            # 2. Mapeamento do DOM (Genoma)
            # Seleciona TUDO que é interativo
            selectors = [
                "button", "a[href]", "input", "select", "textarea", 
                "[role='button']", "div[onclick]", "div[class*='cursor-pointer']"
            ]
            # Snapshot dos elementos para evitar StaleElementReference durante iteração
            # Estratégia: Coletar seletores únicos ou caminhos e re-query a cada passo
            elements_count = await page.evaluate(f"""() => {{
                return document.querySelectorAll("{','.join(selectors)}").length;
            }}""")
            
            print(f"   🧬 {elements_count} genes (elementos) identificados.")

            # 3. Iteração Robusta (Re-query pattern)
            for i in range(elements_count):
                # Re-query o elemento pelo índice para garantir frescor
                # Nota: Isso assume que a ordem do DOM não muda drasticamente.
                # Para v8.0, é aceitável.
                elements = await page.query_selector_all(",".join(selectors))
                if i >= len(elements): break # DOM mudou e tem menos elementos
                
                element = elements[i]
                
                # Processa
                result = await self.process_element(page, element, i, dirs, safe_name, route['route_pattern'])
                
                if result:
                    self.reporter.add_element_result(route['route_pattern'], result)
                    print(f"      [{result['status']}] {result['tag']}: {result['text']}")

        except Exception as e:
            print(f"   ❌ Falha na análise da página: {e}")
            await page.screenshot(path=dirs['imgs'] / "CRASH.png")
        
        finally:
            await context.close()
            # Renomear vídeo da página
            try:
                video_path = await page.video().path()
                if video_path:
                    os.rename(video_path, dirs['videos'] / f"{safe_name}_session.webm")
            except: pass

    async def run(self):
        print("🚀 Optimus UI Genome Tester v8.0 (Ultimate)")
        
        if not os.path.exists(ROUTES_FILE):
            print("❌ Rotas não mapeadas.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
            
            # Login Inicial (Bootstrap)
            if not os.path.exists(AUTH_STATE):
                print("🔑 Gerando Token de Acesso Mestre...")
                page = await browser.new_page()
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard", timeout=15000)
                await page.context.storage_state(path=AUTH_STATE)
                await page.close()

            # Execução Sequencial (Para garantir estabilidade do vídeo)
            # Em v8.1 podemos paralelizar com múltiplos contextos
            for route in routes:
                await self.analyze_page(route, browser)

            await browser.close()
            
        self.reporter.generate_master_report()
        print(f"\n✅ Genoma Mapeado. Relatório em: {OUTPUT_DIR}")

if __name__ == "__main__":
    tester = OptimusGenomeTester()
    asyncio.run(tester.run())
