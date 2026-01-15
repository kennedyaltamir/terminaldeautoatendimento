
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 16:00:00
import asyncio
import os
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# 🧬 OPTIMUS v5.1 — COMPLIANCE GRADE UI EXPLORER (FINAL)
# ==============================================================================
# Protocolo: INDA Strict (Inspection, Normalization, Decision, Action)
# Diferenciais v5.1:
# 1. Diff de DOM Real (SHA-256).
# 2. Seletores Robustos (TestID > ID > Aria).
# 3. Score Decomponível.
# 4. INDA Summary Completo.
# ==============================================================================

BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
OUTPUT_ROOT = Path("testesvisuais")
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
RUN_DIR = OUTPUT_ROOT / f"run_{RUN_ID}"

class IndaLogger:
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.inspection = []
        self.decision = []
        self.action = []
        self.summary = {}

    def log_inspection(self, data): self.inspection.append(data)
    def log_decision(self, data): self.decision.append(data)
    def log_action(self, data): self.action.append(data)
    
    def set_summary(self, data): self.summary = data

    def save(self):
        for name, data in [
            ("inda_inspection.json", self.inspection),
            ("inda_decision.json", self.decision),
            ("inda_action.json", self.action),
            ("inda_summary.json", self.summary)
        ]:
            with open(self.docs_dir / name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

class DomHasher:
    @staticmethod
    async def compute(page: Page):
        # Hash do body limpo (sem scripts/styles para evitar ruído)
        content = await page.evaluate("""() => {
            const clone = document.body.cloneNode(true);
            const scripts = clone.querySelectorAll('script, style, noscript');
            scripts.forEach(el => el.remove());
            return clone.innerHTML;
        }""")
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

class SelectorEngine:
    @staticmethod
    async def resolve(handle):
        # Tenta estratégias em ordem de robustez
        try:
            # 1. Data Test ID
            test_id = await handle.get_attribute("data-testid")
            if test_id: return f"[data-testid='{test_id}']"
            
            # 2. ID
            el_id = await handle.get_attribute("id")
            if el_id: return f"#{el_id}"
            
            # 3. Aria Label
            aria = await handle.get_attribute("aria-label")
            if aria: return f"[aria-label='{aria}']"
            
            # 4. Fallback: Tag + Text (Frágil, mas útil)
            tag = await handle.evaluate("el => el.tagName.toLowerCase()")
            text = (await handle.inner_text()).strip()[:20]
            if text: return f"{tag}:has-text('{text}')"
            
            return "unknown"
        except:
            return "error"

class PageAuditor:
    def __init__(self, browser, route_data: dict, mode: str):
        self.browser = browser
        self.route_data = route_data
        self.mode = mode
        self.url = f"{BASE_URL}{route_data['test_url']}"
        self.page_name = route_data['route_pattern'].replace("/", "_").strip("_") or "home"
        
        self.base_dir = RUN_DIR / self.page_name
        self.docs_dir = self.base_dir / "docs"
        self.imgs_dir = self.base_dir / "imgs"
        self.video_dir = self.base_dir / "videos"
        
        self._setup_dirs()
        self.inda = IndaLogger(self.docs_dir)

    def _setup_dirs(self):
        for d in [self.docs_dir, self.imgs_dir / "full", self.imgs_dir / "elements", self.video_dir]:
            d.mkdir(parents=True, exist_ok=True)

    async def run(self):
        print(f"🔭 Auditando: {self.page_name} ({self.url})")
        
        context = await self.browser.new_context(
            record_video_dir=str(self.video_dir),
            viewport={"width": 1280, "height": 720}
        )
        
        await self._inject_auth(context)
        page = await context.new_page()
        
        try:
            # 1. INSPECTION
            response = await page.goto(self.url, wait_until="networkidle", timeout=20000)
            status = response.status if response else 0
            
            await self._smooth_scroll(page)
            await page.screenshot(path=self.imgs_dir / "full" / "before.png", full_page=True)
            initial_hash = await DomHasher.compute(page)
            
            elements = await self._scan_elements(page)
            self.inda.log_inspection({
                "url": self.url, 
                "status": status, 
                "dom_hash": initial_hash,
                "elements_count": len(elements)
            })

            # 2. NORMALIZATION & DECISION
            results = []
            for el in elements:
                decision = self._decide_interaction(el)
                self.inda.log_decision(decision)
                
                # 3. ACTION (Behavioral)
                if self.mode in ['behavioral', 'demo']:
                    # Resolve handle fresco para evitar stale element
                    try:
                        handle = page.locator(el['selector']).first
                        if await handle.count() > 0:
                            result = await self._execute_interaction(page, handle, el, decision, initial_hash)
                            results.append(result)
                            self.inda.log_action(result)
                        else:
                            results.append({**el, "result": "STALE", "verdict": "SKIPPED"})
                    except Exception as e:
                        results.append({**el, "result": "ERROR", "error": str(e)})
                else:
                    results.append({**el, "result": "SKIPPED"})

            # 4. REPORTING & SCORING
            score_data = self._calculate_score(results, status)
            
            summary = {
                "page": self.page_name,
                "url": self.url,
                "timestamp": datetime.now().isoformat(),
                "status_http": status,
                "score": score_data,
                "risk": "HIGH" if score_data['total'] < 70 else "LOW",
                "elements_total": len(elements),
                "interactions_success": len([r for r in results if r.get('verdict') == 'SUCCESS'])
            }
            
            self.inda.set_summary(summary)
            self.inda.save()
            self._generate_markdown(results, status, score_data)
            
        except Exception as e:
            print(f"   ❌ Erro em {self.page_name}: {e}")
        finally:
            await context.close()
            try:
                video_file = list(self.video_dir.glob("*.webm"))[0]
                video_file.rename(self.video_dir / "walkthrough.webm")
            except: pass

    async def _inject_auth(self, context):
        token = os.getenv("MESAFLOW_TEST_TOKEN", "fake-jwt-token-for-testing")
        await context.add_init_script(f"""
            localStorage.setItem('mesaflow_access_token', '{token}');
            localStorage.setItem('mesaflow_user_role', 'owner');
            localStorage.setItem('mesaflow_tour_completed', 'true');
        """)

    async def _smooth_scroll(self, page: Page):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        await page.evaluate("window.scrollTo(0, 0)")

    async def _scan_elements(self, page: Page):
        selectors = ["button", "a[href]", "input:not([type='hidden'])", "[role='button']"]
        elements = []
        handles = await page.query_selector_all(", ".join(selectors))
        
        for i, handle in enumerate(handles):
            if not await handle.is_visible(): continue
            
            box = await handle.bounding_box()
            if not box: continue
            
            tag = await handle.evaluate("el => el.tagName.toLowerCase()")
            text = (await handle.inner_text()).strip()[:30].replace("\n", " ") or "Sem Texto"
            selector = await SelectorEngine.resolve(handle)
            
            el_id = f"{tag}_{i}_{hashlib.md5(selector.encode()).hexdigest()[:6]}"
            
            # Screenshot
            await handle.screenshot(path=self.imgs_dir / "elements" / f"{el_id}.png")
            
            elements.append({
                "id": el_id,
                "tag": tag,
                "text": text,
                "selector": selector,
                "classification": "PRIMARY_ACTION" if tag == "button" else "NAVIGATION" if tag == "a" else "INPUT"
            })
        return elements

    def _decide_interaction(self, element):
        action = "hover"
        if element['tag'] == "input": action = "fill"
        elif element['tag'] == "a": action = "navigation"
        
        return {
            "element_id": element['id'],
            "planned_action": action,
            "risk": "LOW"
        }

    async def _execute_interaction(self, page: Page, handle, element, decision, initial_hash):
        before_url = page.url
        
        try:
            if decision['planned_action'] == "fill":
                await handle.fill("Test", timeout=1000)
            else:
                await handle.hover(timeout=1000)
                
            # Pós-Interação
            after_url = page.url
            after_hash = await DomHasher.compute(page)
            
            url_changed = before_url != after_url
            dom_changed = initial_hash != after_hash
            
            verdict = "SUCCESS"
            if not url_changed and not dom_changed and decision['planned_action'] != "hover":
                verdict = "NO_EFFECT"
                
            return {
                **element,
                "verdict": verdict,
                "diff": {
                    "url_changed": url_changed,
                    "dom_changed": dom_changed
                }
            }
            
        except Exception as e:
            return {**element, "verdict": "BROKEN", "error": str(e)}

    def _calculate_score(self, results, status):
        http_score = 40 if status == 200 else 0
        
        total_els = len(results)
        if total_els == 0: return {"total": http_score + 60, "http": http_score, "functional": 60}
        
        broken = len([r for r in results if r.get('verdict') == 'BROKEN'])
        functional_score = int(60 * (1 - (broken / total_els)))
        
        return {
            "total": http_score + functional_score,
            "http": http_score,
            "functional": functional_score,
            "ux_feedback": 0 # Placeholder para v6
        }

    def _generate_markdown(self, results, status, score):
        with open(self.docs_dir / "relatorio.md", "w", encoding="utf-8") as f:
            f.write(f"# 🕵️ Relatório de Auditoria: {self.page_name}\n")
            f.write(f"**Score Global:** {score['total']}/100\n")
            f.write(f"- HTTP: {score['http']}/40\n")
            f.write(f"- Funcional: {score['functional']}/60\n\n")
            
            f.write("## 🧪 Matriz de Testes\n")
            f.write("| ID | Elemento | Ação | Veredito | Diff |\n")
            f.write("|---|---|---|---|---|\n")
            for r in results:
                icon = "✅" if r.get('verdict') == 'SUCCESS' else "⚠️" if r.get('verdict') == 'NO_EFFECT' else "❌"
                diff = "DOM" if r.get('diff', {}).get('dom_changed') else "URL" if r.get('diff', {}).get('url_changed') else "-"
                f.write(f"| {r['id']} | `{r['tag']}` {r['text']} | {r.get('planned_action', '-')} | {icon} {r.get('verdict')} | {diff} |\n")

class EnterpriseExplorerV5_1:
    async def run(self, mode="behavioral"):
        print(f"🚀 Iniciando Optimus v5.1 (Mode: {mode})...")
        
        if not os.path.exists(ROUTES_FILE):
            print("❌ Erro: mapped_routes.json não encontrado.")
            return

        with open(ROUTES_FILE, "r", encoding="utf-8") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            for route in routes:
                auditor = PageAuditor(browser, route, mode)
                await auditor.run()

            await browser.close()
            print(f"\n✅ Execução concluída. Artefatos em: {RUN_DIR}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["inventory", "behavioral", "demo"], default="behavioral")
    args = parser.parse_args()
    
    explorer = EnterpriseExplorerV5_1()
    asyncio.run(explorer.run(args.mode))

