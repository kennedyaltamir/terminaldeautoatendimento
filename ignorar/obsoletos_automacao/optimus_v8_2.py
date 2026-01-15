import asyncio
import os
import json
import random
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator
from faker import Faker

# ==============================================================================
# 🧬 OPTIMUS v8.2 — MODAL RESILIENT EDITION
# ==============================================================================
# Atualização Crítica:
# 1. Modal Hunter: Detecta e fecha popups, modais e overlays bloqueantes.
# 2. Interception Recovery: Se um clique for interceptado, tenta limpar a tela e retentar.
# 3. Joyride Killer: Remove proativamente elementos de tour guiado.
# ==============================================================================

BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
OUTPUT_DIR = Path("testesvisuais")
GLOBAL_DIR = OUTPUT_DIR / "_global"
AUTH_STATE = "auth_state.json"

fake = Faker('pt_BR')

MODES = {
    "A": {"name": "Preciso e Matemático", "retries": 2, "destructive": False, "precision": "high"},
    "B": {"name": "Criativo e Explorador", "retries": 3, "destructive": False, "precision": "medium"},
    "C": {"name": "Cognitivo e Inteligente", "retries": 3, "destructive": False, "precision": "human"},
    "D": {"name": "Brutal e Completo", "retries": 5, "destructive": True, "precision": "force"},
    "E": {"name": "Híbrido Inteligente", "retries": 3, "destructive": False, "precision": "adaptive"}
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
        filename = f"{name}.png"
        path = self.imgs_dir / filename
        try:
            if element and highlight:
                if await element.is_visible():
                    await element.evaluate("el => { el.style.outline = '3px solid #ea580c'; el.style.boxShadow = '0 0 0 4px rgba(234, 88, 12, 0.3)'; }")
            
            await page.screenshot(path=path)
            
            if element and highlight:
                if await element.is_visible():
                    await element.evaluate("el => { el.style.outline = ''; el.style.boxShadow = ''; }")
        except Exception as e:
            print(f"   ⚠️ Erro ao capturar screenshot: {e}")
        return str(path)

class InteractionEngine:
    def __init__(self, page: Page, mode_config: dict):
        self.page = page
        self.config = mode_config

    async def inject_laser_pointer(self):
        await self.page.evaluate("""() => {
            if (document.getElementById('optimus-laser')) return;
            const laser = document.createElement('div');
            laser.id = 'optimus-laser';
            laser.style.position = 'fixed';
            laser.style.width = '10px';
            laser.style.height = '10px';
            laser.style.backgroundColor = 'red';
            laser.style.borderRadius = '50%';
            laser.style.zIndex = '2147483647';
            laser.style.pointerEvents = 'none';
            document.body.appendChild(laser);
            window.addEventListener('mousemove', (e) => {
                laser.style.left = e.clientX + 'px';
                laser.style.top = e.clientY + 'px';
            });
        }""")

    async def clear_overlays(self):
        """
        🛡️ MODAL HUNTER: Identifica e fecha elementos bloqueantes conhecidos.
        """
        blockers = [
            # Botões de Fechar Genéricos
            "button[aria-label='Close']",
            "button[aria-label='Fechar']",
            ".lucide-x", # Ícone X comum
            
            # Modais Específicos do Projeto
            ".react-joyride__overlay", # Tour
            "#react-joyride-portal",
            "button:has-text('Entendi')",
            "button:has-text('Aceitar')", # Cookies
            "button:has-text('Agora não')",
            
            # Lead Capture / Popups
            "div[class*='fixed inset-0'] button:has(svg)", # Botão X dentro de modal Tailwind
        ]

        found_blocker = False
        for selector in blockers:
            try:
                # Verifica se existe e está visível
                if await self.page.locator(selector).first.is_visible(timeout=200):
                    print(f"   🧹 Removendo bloqueio detectado: {selector}")
                    # Tenta clicar
                    await self.page.locator(selector).first.click(timeout=500, force=True)
                    await self.page.wait_for_timeout(300)
                    found_blocker = True
            except:
                pass
        
        # Se encontrou algo, espera a animação de saída
        if found_blocker:
            await self.page.wait_for_timeout(500)

    async def smart_click(self, element: Locator, intent: str):
        strategies = ["standard", "clear_and_retry", "force", "js"]
        
        for strategy in strategies:
            try:
                if strategy == "standard":
                    await element.scroll_into_view_if_needed()
                    await element.click(timeout=1500)
                
                elif strategy == "clear_and_retry":
                    # Se o standard falhou (provavelmente interceptado), limpa a tela
                    print("      🛡️ Tentando limpar overlays e retentar...")
                    await self.clear_overlays()
                    await element.scroll_into_view_if_needed()
                    await element.click(timeout=1500)

                elif strategy == "force":
                    await element.click(force=True, timeout=1500)
                
                elif strategy == "js":
                    await element.evaluate("el => el.click()")
                
                return {"success": True, "strategy": strategy}
            
            except Exception as e:
                # Se o erro for explicitamente de interceptação, tenta limpar imediatamente
                if "intercepts pointer events" in str(e):
                    await self.clear_overlays()
                continue
        
        return {"success": False, "error": "All strategies failed"}

class CognitiveBrain:
    def analyze_element(self, tag, text, type_attr, aria_label):
        context = f"{text} {aria_label} {type_attr}".lower()
        analysis = {
            "intent": "interaction",
            "risk": "low",
            "priority": "P3",
            "expected_behavior": "Change UI State"
        }
        
        if any(x in context for x in ["excluir", "remover", "delete", "trash"]):
            analysis.update({"intent": "destructive", "risk": "high", "priority": "P1"})
        elif any(x in context for x in ["salvar", "entrar", "login", "enviar", "cadastrar"]):
            analysis.update({"intent": "submission", "priority": "P0"})
        elif any(x in context for x in ["voltar", "cancelar"]):
            analysis.update({"intent": "navigation_back", "priority": "P2"})
        elif tag == "input":
            analysis.update({"intent": "data_entry", "priority": "P1"})
            
        return analysis

class OptimusV8_2:
    def __init__(self, mode_key="E"):
        self.mode_key = mode_key
        self.config = MODES[mode_key]
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.global_stats = {"pages": 0, "elements": 0, "score_sum": 0}
        self.setup_global()

    def setup_global(self):
        GLOBAL_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\n🤖 OPTIMUS v8.2 (Modal Resilient) INICIADO")
        print(f"🔥 MODO: {self.config['name']}")
        print(f"📂 Output: {OUTPUT_DIR}/run_{self.run_id}")

    async def run(self):
        if not os.path.exists(ROUTES_FILE):
            print("❌ Rotas não mapeadas.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            # Headless=False para debug visual se necessário, ou True para CI
            browser = await p.chromium.launch(headless=True, slow_mo=100)
            
            if not os.path.exists(AUTH_STATE):
                print("🔑 Realizando Login Administrativo...")
                page = await browser.new_page()
                try:
                    await page.goto(f"{BASE_URL}/admin/login")
                    await page.fill('input[name="email"]', "admin@mesaflow.com")
                    await page.fill('input[name="password"]', "123456")
                    await page.click('button[type="submit"]')
                    await page.wait_for_url("**/dashboard", timeout=15000)
                    await page.context.storage_state(path=AUTH_STATE)
                except Exception as e:
                    print(f"⚠️ Falha no login inicial: {e}")
                await page.close()

            for route in routes:
                await self.process_page(route, browser)

            await browser.close()
            self.generate_global_report()

    async def process_page(self, route, browser):
        url = f"{BASE_URL}{route['test_url']}"
        safe_name = route['route_pattern'].replace("/", "_").strip("_") or "home"
        page_dir = OUTPUT_DIR / f"run_{self.run_id}" / safe_name
        evidence = EvidenceManager(page_dir)
        
        print(f"\n🔭 Analisando: {url}")
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir=evidence.videos_dir,
            record_video_size={"width": 1280, "height": 800},
            storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None
        )
        
        # Script para limpar Joyride automaticamente se aparecer
        await context.add_init_script("""
            window.localStorage.setItem('mesaflow_tour_completed', 'true');
            window.sessionStorage.setItem('mesaflow_lead_popup', 'true');
        """)
        
        page = await context.new_page()
        engine = InteractionEngine(page, self.config)
        brain = CognitiveBrain()
        
        page_report = {"url": url, "elements": [], "score": 100, "issues": []}

        try:
            await page.goto(url, wait_until="networkidle", timeout=20000)
            await engine.inject_laser_pointer()
            
            # Limpeza Preventiva de Modais ao Carregar
            await engine.clear_overlays()
            
            await evidence.capture_screenshot(page, "00_fullpage_start")

            selectors = "button:visible, a[href]:visible, input:visible, textarea:visible, [role='button']:visible"
            elements = await page.query_selector_all(selectors)
            print(f"   🧩 {len(elements)} elementos detectados.")

            # Limite de segurança para não travar em páginas gigantes
            for i, handle in enumerate(elements[:30]): 
                try:
                    if not await handle.is_visible(): continue
                    
                    tag = await handle.evaluate("el => el.tagName.toLowerCase()")
                    text = (await handle.inner_text()).strip().replace("\n", " ")[:30]
                    type_attr = await handle.get_attribute("type") or ""
                    aria_label = await handle.get_attribute("aria-label") or ""
                    
                    analysis = brain.analyze_element(tag, text, type_attr, aria_label)
                    el_id = f"el_{i:03d}"

                    if analysis["risk"] == "high" and not self.config["destructive"]:
                        page_report["elements"].append({"id": el_id, "text": text, "status": "SKIPPED_SAFETY"})
                        continue

                    # Interação
                    await evidence.capture_screenshot(page, f"{el_id}_before", handle, highlight=True)
                    
                    result = {"success": False}
                    if analysis["intent"] == "data_entry":
                        await handle.fill(fake.word())
                        result = {"success": True, "strategy": "fill"}
                    else:
                        result = await engine.smart_click(handle, analysis["intent"])

                    await page.wait_for_timeout(300)
                    
                    # Se navegou, volta
                    if page.url != url:
                        try:
                            await page.go_back(wait_until="domcontentloaded")
                            await engine.inject_laser_pointer()
                            await engine.clear_overlays() # Limpa de novo ao voltar
                        except: pass

                    status = "SUCCESS" if result["success"] else "FAILURE"
                    if status == "FAILURE":
                        page_report["score"] -= 5
                        print(f"      ❌ Falha em: {text}")

                    page_report["elements"].append({
                        "id": el_id, "tag": tag, "text": text, 
                        "result": result, "status": status
                    })

                except Exception as el_err:
                    print(f"      ⚠️ Erro no elemento {i}: {el_err}")

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
            try:
                video_path = await page.video().path()
                if video_path:
                    os.rename(video_path, evidence.videos_dir / f"{safe_name}_audit.webm")
            except: pass

    def generate_page_report(self, docs_dir, data):
        with open(docs_dir / "relatorio_pagina.md", "w", encoding="utf-8") as f:
            f.write(f"# 📄 Relatório: {data['url']}\n")
            f.write(f"**Score:** {data['score']}/100\n\n")
            f.write("| ID | Elemento | Estratégia | Status |\n|---|---|---|---|\n")
            for el in data['elements']:
                strat = el.get('result', {}).get('strategy', '-')
                f.write(f"| {el['id']} | **{el.get('text', '')}** | {strat} | {el['status']} |\n")

    def generate_global_report(self):
        avg = self.global_stats["score_sum"] / self.global_stats["pages"] if self.global_stats["pages"] > 0 else 0
        with open(GLOBAL_DIR / "relatorio_global.md", "w", encoding="utf-8") as f:
            f.write(f"# 🌍 Relatório Global v8.2\n**Score Médio:** {avg:.1f}/100\n")
            f.write(f"**Páginas:** {self.global_stats['pages']} | **Elementos:** {self.global_stats['elements']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='E', choices=['A', 'B', 'C', 'D', 'E'])
    args = parser.parse_args()
    auditor = OptimusV8_2(mode_key=args.mode)
    asyncio.run(auditor.run())
