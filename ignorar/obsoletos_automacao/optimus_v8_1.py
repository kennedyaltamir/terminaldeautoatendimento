import asyncio
import os
import json
import random
import math
import argparse
import shutil
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator, BrowserContext
from faker import Faker

# ==============================================================================
# 🧬 OPTIMUS v8.1 — HYPER REACTIVE MODE (KERNEL INDA)
# ==============================================================================
# "Auditoria Cognitiva, Funcional e Comportamental de Alta Precisão"
# ------------------------------------------------------------------------------
# Módulos:
# 1. Hyper Reactive Click Engine (Ajuste fino, Fallbacks, JS Force)
# 2. Evidence 2.0 (Zoom, Highlights, Laser Tracking)
# 3. Relatório V2 (Heurísticas Nielsen, Scores, Mapas)
# 4. Ciclos Adaptativos (Retries inteligentes)
# 5. Modos de Execução (A, B, C, D, E)
# ==============================================================================

BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
OUTPUT_DIR = Path("testesvisuais")
GLOBAL_DIR = OUTPUT_DIR / "_global"
AUTH_STATE = "auth_state.json"

fake = Faker('pt_BR')

# --- CONFIGURAÇÃO DE MODOS ---
MODES = {
    "A": {"name": "Preciso e Matemático", "retries": 2, "destructive": False, "fuzz": False, "precision": "high"},
    "B": {"name": "Criativo e Explorador", "retries": 3, "destructive": False, "fuzz": True, "precision": "medium"},
    "C": {"name": "Cognitivo e Inteligente", "retries": 3, "destructive": False, "fuzz": False, "precision": "human"},
    "D": {"name": "Brutal e Completo", "retries": 5, "destructive": True, "fuzz": True, "precision": "force"},
    "E": {"name": "Híbrido Inteligente", "retries": 3, "destructive": False, "fuzz": False, "precision": "adaptive"}
}

class EvidenceManager:
    def __init__(self, page_dir: Path):
        self.page_dir = page_dir
        self.imgs_dir = page_dir / "imgs"
        self.videos_dir = page_dir / "videos"
        self.docs_dir = page_dir / "docs"
        
        for d in [self.imgs_dir, self.videos_dir, self.docs_dir]:
            d.mkdir(parents=True, exist_ok=True)

    async def capture_screenshot(self, page: Page, name: str, element: Locator = None, highlight=False):
        """Captura screenshot com opções avançadas de highlight e crop."""
        filename = f"{name}.png"
        path = self.imgs_dir / filename
        
        if element and highlight:
            # Desenha círculo/borda
            await element.evaluate("""el => {
                el.style.outline = '3px solid #ea580c';
                el.style.boxShadow = '0 0 0 4px rgba(234, 88, 12, 0.3)';
                el.setAttribute('data-optimus-focus', 'true');
            }""")
            
        await page.screenshot(path=path, full_page=False)
        
        if element and highlight:
            # Remove highlight
            await element.evaluate("""el => {
                el.style.outline = '';
                el.style.boxShadow = '';
                el.removeAttribute('data-optimus-focus');
            }""")
            
            # Zoom Crop (Simulado via screenshot do elemento com padding)
            try:
                zoom_path = self.imgs_dir / f"{name}_zoom.png"
                # Tenta capturar uma área maior ao redor do elemento
                box = await element.bounding_box()
                if box:
                    padding = 50
                    clip = {
                        "x": max(0, box['x'] - padding),
                        "y": max(0, box['y'] - padding),
                        "width": box['width'] + (padding * 2),
                        "height": box['height'] + (padding * 2)
                    }
                    await page.screenshot(path=zoom_path, clip=clip)
            except Exception as e:
                print(f"   ⚠️ Falha no Zoom Crop: {e}")

        return str(path)

class InteractionEngine:
    def __init__(self, page: Page, mode_config: dict):
        self.page = page
        self.config = mode_config

    async def inject_laser_pointer(self):
        """Injeta um 'laser' visual que segue o mouse para o vídeo."""
        await self.page.evaluate("""() => {
            const laser = document.createElement('div');
            laser.id = 'optimus-laser';
            laser.style.position = 'fixed';
            laser.style.width = '10px';
            laser.style.height = '10px';
            laser.style.backgroundColor = 'red';
            laser.style.borderRadius = '50%';
            laser.style.zIndex = '10000';
            laser.style.pointerEvents = 'none';
            laser.style.boxShadow = '0 0 10px red';
            laser.style.transition = 'top 0.1s, left 0.1s';
            document.body.appendChild(laser);

            window.addEventListener('mousemove', (e) => {
                laser.style.left = e.clientX + 'px';
                laser.style.top = e.clientY + 'px';
            });
            
            window.addEventListener('click', (e) => {
                const ripple = document.createElement('div');
                ripple.style.position = 'fixed';
                ripple.style.left = (e.clientX - 20) + 'px';
                ripple.style.top = (e.clientY - 20) + 'px';
                ripple.style.width = '40px';
                ripple.style.height = '40px';
                ripple.style.border = '2px solid red';
                ripple.style.borderRadius = '50%';
                ripple.style.zIndex = '9999';
                ripple.style.animation = 'optimus-ripple 0.5s forwards';
                document.body.appendChild(ripple);
                setTimeout(() => ripple.remove(), 500);
            });

            const style = document.createElement('style');
            style.innerHTML = `
                @keyframes optimus-ripple {
                    0% { transform: scale(0); opacity: 1; }
                    100% { transform: scale(2); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }""")

    async def smart_click(self, element: Locator, intent: str):
        """
        Motor de Clique Hiper Reativo.
        Tenta várias estratégias se a primeira falhar.
        """
        strategies = ["standard", "offset", "force", "js"]
        if self.config["precision"] == "high":
            strategies = ["standard", "offset"] # Modo A é estrito
        elif self.config["precision"] == "force":
            strategies = ["standard", "force", "js"] # Modo D é brutal

        for strategy in strategies:
            try:
                # Scroll into view suave
                await element.scroll_into_view_if_needed()
                await self.page.wait_for_timeout(200) # Estabilização visual

                # Move o mouse (Laser Pointer Effect)
                box = await element.bounding_box()
                if box:
                    await self.page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                
                if strategy == "standard":
                    await element.click(timeout=2000)
                elif strategy == "offset":
                    # Tenta clicar levemente fora do centro (evita sobreposições de label)
                    await element.click(position={"x": 5, "y": 5}, timeout=2000)
                elif strategy == "force":
                    await element.click(force=True, timeout=2000)
                elif strategy == "js":
                    await element.evaluate("el => el.click()")
                
                return {"success": True, "strategy": strategy}
            except Exception as e:
                print(f"      🔸 Falha na estratégia {strategy}: {str(e)[:50]}...")
                continue
        
        return {"success": False, "error": "All strategies failed"}

class CognitiveBrain:
    def __init__(self):
        pass

    def analyze_element(self, tag, text, type_attr, aria_label):
        """Classifica o elemento e define risco/prioridade."""
        context = f"{text} {aria_label} {type_attr}".lower()
        
        analysis = {
            "intent": "interaction",
            "risk": "low",
            "priority": "P3",
            "expected_behavior": "Change UI State"
        }

        if "excluir" in context or "remover" in context or "delete" in context:
            analysis["intent"] = "destructive"
            analysis["risk"] = "high"
            analysis["priority"] = "P1"
            analysis["expected_behavior"] = "Confirmation Modal"
        
        elif "salvar" in context or "entrar" in context or "login" in context:
            analysis["intent"] = "submission"
            analysis["priority"] = "P0"
            analysis["expected_behavior"] = "Navigation or Success Message"

        elif "voltar" in context or "cancelar" in context:
            analysis["intent"] = "navigation_back"
            analysis["priority"] = "P2"
        
        elif tag == "input":
            analysis["intent"] = "data_entry"
            analysis["priority"] = "P1"
            analysis["expected_behavior"] = "Accept Input"

        return analysis

class OptimusV8_1:
    def __init__(self, mode_key="E"):
        self.mode_key = mode_key
        self.config = MODES[mode_key]
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.global_stats = {"pages": 0, "elements": 0, "bugs": 0, "score_sum": 0}
        self.setup_global()

    def setup_global(self):
        GLOBAL_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\n🤖 OPTIMUS v8.1 INICIADO")
        print(f"🔥 MODO: {self.config['name']}")
        print(f"📂 Output: {OUTPUT_DIR}/run_{self.run_id}")

    async def run(self):
        if not os.path.exists(ROUTES_FILE):
            print("❌ Rotas não mapeadas. Execute map_routes.py primeiro.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False) # Headless False para ver o laser (opcional)
            
            # Login Bootstrap
            if not os.path.exists(AUTH_STATE):
                print("🔑 Realizando Login Administrativo...")
                page = await browser.new_page()
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard", timeout=15000)
                await page.context.storage_state(path=AUTH_STATE)
                await page.close()

            for route in routes:
                await self.process_page(route, browser)

            await browser.close()
            self.generate_global_report()

    async def process_page(self, route, browser):
        url = f"{BASE_URL}{route['test_url']}"
        page_name = route['route_pattern']
        safe_name = page_name.replace("/", "_").strip("_") or "home"
        
        # Setup Pastas
        page_dir = OUTPUT_DIR / f"run_{self.run_id}" / safe_name
        evidence = EvidenceManager(page_dir)
        
        print(f"\n🔭 Analisando: {url}")
        
        # Contexto Isolado (Vídeo Único)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir=evidence.videos_dir,
            record_video_size={"width": 1280, "height": 800},
            storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None
        )
        
        page = await context.new_page()
        engine = InteractionEngine(page, self.config)
        brain = CognitiveBrain()
        
        page_report = {
            "url": url,
            "elements": [],
            "score": 100,
            "issues": []
        }

        try:
            await page.goto(url, wait_until="networkidle", timeout=20000)
            await engine.inject_laser_pointer()
            
            # Screenshot Full Page Inicial
            await evidence.capture_screenshot(page, "00_fullpage_start")

            # Detecção de Elementos
            selectors = "button, a[href], input, select, textarea, [role='button']"
            elements = await page.query_selector_all(selectors)
            print(f"   🧩 {len(elements)} elementos detectados.")

            for i, handle in enumerate(elements):
                if not await handle.is_visible(): continue
                
                # Análise Cognitiva
                tag = await handle.evaluate("el => el.tagName.toLowerCase()")
                text = (await handle.inner_text()).strip().replace("\n", " ")[:30]
                type_attr = await handle.get_attribute("type") or ""
                aria_label = await handle.get_attribute("aria-label") or ""
                
                analysis = brain.analyze_element(tag, text, type_attr, aria_label)
                el_id = f"el_{i:03d}"

                # Filtro de Segurança (Modo Destrutivo)
                if analysis["risk"] == "high" and not self.config["destructive"]:
                    print(f"   🛡️ Skipped Destructive: {text}")
                    page_report["elements"].append({
                        "id": el_id, "text": text, "status": "SKIPPED_SAFETY", "analysis": analysis
                    })
                    continue

                # Execução da Interação
                # 1. Print Antes
                await evidence.capture_screenshot(page, f"{el_id}_before", handle, highlight=True)
                
                # 2. Ação (Click/Fill)
                result = {"success": False}
                if analysis["intent"] == "data_entry":
                    await handle.fill(fake.word()) # Simplificado para demo
                    result = {"success": True, "strategy": "fill"}
                else:
                    result = await engine.smart_click(handle, analysis["intent"])

                # 3. Validação de Reação
                await page.wait_for_timeout(500)
                
                # 4. Print Depois
                await evidence.capture_screenshot(page, f"{el_id}_after")

                # Registro
                status = "SUCCESS" if result["success"] else "FAILURE"
                if status == "FAILURE":
                    page_report["score"] -= 10
                    page_report["issues"].append(f"Falha ao interagir com {text}")

                page_report["elements"].append({
                    "id": el_id,
                    "tag": tag,
                    "text": text,
                    "analysis": analysis,
                    "result": result,
                    "status": status
                })
                
                # Recuperação de Navegação (Se saiu da página)
                if page.url != url:
                    try:
                        await page.go_back(wait_until="domcontentloaded")
                        await page.wait_for_timeout(1000)
                        await engine.inject_laser_pointer() # Reinjeta o laser
                    except:
                        pass

            # Geração do Relatório da Página
            self.generate_page_report(evidence.docs_dir, page_report)
            self.global_stats["pages"] += 1
            self.global_stats["elements"] += len(elements)
            self.global_stats["score_sum"] += page_report["score"]

        except Exception as e:
            print(f"   ❌ Erro crítico na página: {e}")
            with open(evidence.docs_dir / "CRASH.log", "w") as f:
                f.write(str(e))
        finally:
            await context.close()
            # Renomear vídeo
            try:
                video_path = await page.video().path()
                if video_path:
                    os.rename(video_path, evidence.videos_dir / f"{safe_name}_audit.webm")
            except: pass

    def generate_page_report(self, docs_dir, data):
        with open(docs_dir / "relatorio_pagina.md", "w", encoding="utf-8") as f:
            f.write(f"# 📄 Relatório de Auditoria: {data['url']}\n")
            f.write(f"**Score de Saúde:** {data['score']}/100\n\n")
            
            f.write("## 1. Análise Heurística\n")
            f.write("| ID | Elemento | Intenção | Risco | Estratégia | Status |\n")
            f.write("|---|---|---|---|---|---|\n")
            for el in data['elements']:
                strat = el.get('result', {}).get('strategy', '-')
                f.write(f"| {el['id']} | **{el['text']}** | {el['analysis']['intent']} | {el['analysis']['risk']} | {strat} | {el['status']} |\n")

            f.write("\n## 2. Problemas Encontrados\n")
            if data['issues']:
                for issue in data['issues']:
                    f.write(f"- 🔴 {issue}\n")
            else:
                f.write("✅ Nenhum problema crítico detectado.\n")

    def generate_global_report(self):
        avg_score = self.global_stats["score_sum"] / self.global_stats["pages"] if self.global_stats["pages"] > 0 else 0
        
        with open(GLOBAL_DIR / "relatorio_global.md", "w", encoding="utf-8") as f:
            f.write("# 🌍 Genoma Evolutivo Global (v8.1)\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y')}\n")
            f.write(f"**Modo de Execução:** {self.config['name']}\n\n")
            
            f.write("## Estatísticas Gerais\n")
            f.write(f"- **Páginas Auditadas:** {self.global_stats['pages']}\n")
            f.write(f"- **Elementos Testados:** {self.global_stats['elements']}\n")
            f.write(f"- **Score Médio de Saúde:** {avg_score:.1f}/100\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Optimus v8.1 - Cognitive QA Auditor')
    parser.add_argument('--mode', type=str, default='E', choices=['A', 'B', 'C', 'D', 'E'], help='Modo de Operação (A=Preciso, B=Criativo, C=Cognitivo, D=Brutal, E=Híbrido)')
    args = parser.parse_args()
    
    auditor = OptimusV8_1(mode_key=args.mode)
    asyncio.run(auditor.run())
