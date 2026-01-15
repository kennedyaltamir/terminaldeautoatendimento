import asyncio
import os
import json
import time
import random
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator
from faker import Faker

# ==============================================================================
# 🏗️ CONFIGURAÇÃO OPTIMUS ARCHITECT (V5.0)
# ==============================================================================
BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
OUTPUT_DIR = Path("testesvisuais")
AUTH_STATE = "auth_state.json"

# Configurações de Comportamento
SLOW_MO = 1000  # ms (Lentidão para vídeo humano)
SCROLL_STEPS = 10
INTERACTION_DELAY = 1.5 # segundos

fake = Faker('pt_BR')

class OptimusVisualTester:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_data = {}
        
    def setup_page_dirs(self, page_name: str):
        """Cria a estrutura de pastas exigida: docs, imgs, videos."""
        safe_name = page_name.replace("/", "_").strip("_") or "home"
        base = OUTPUT_DIR / safe_name
        
        dirs = {
            "root": base,
            "docs": base / "docs",
            "imgs": base / "imgs",
            "videos": base / "videos"
        }
        
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
            
        return dirs, safe_name

    async def smooth_scroll(self, page: Page):
        """Realiza rolagem suave para capturar vídeo e carregar lazy components."""
        print("   📜 Executando rolagem suave para análise completa...")
        await page.evaluate(f"""async () => {{
            const totalHeight = document.body.scrollHeight;
            const distance = 100;
            const timer = (ms) => new Promise(res => setTimeout(res, ms));
            
            for (let scrolled = 0; scrolled < totalHeight; scrolled += distance) {{
                window.scrollBy(0, distance);
                await timer(100);
            }}
            // Voltar ao topo
            window.scrollTo(0, 0);
        }}""")
        await page.wait_for_timeout(1000)

    async def highlight_element(self, locator: Locator, color="red"):
        """Destaca visualmente um elemento para o print."""
        try:
            await locator.evaluate(f"el => el.style.outline = '3px solid {color}'")
            await locator.evaluate(f"el => el.style.boxShadow = '0 0 10px {color}'")
        except:
            pass

    async def unhighlight_element(self, locator: Locator):
        """Remove o destaque."""
        try:
            await locator.evaluate("el => el.style.outline = ''")
            await locator.evaluate("el => el.style.boxShadow = ''")
        except:
            pass

    async def analyze_accessibility(self, page: Page):
        """Executa heurísticas de acessibilidade e UX."""
        return await page.evaluate("""() => {
            const issues = [];
            const elements = document.querySelectorAll('button, a, input, select, textarea');
            
            elements.forEach(el => {
                // 1. Contraste (Heurística simples)
                const style = window.getComputedStyle(el);
                if (style.opacity < 0.5) issues.push(`Baixa opacidade em ${el.tagName}: ${style.opacity}`);
                
                // 2. Tamanho do Alvo (Touch Target)
                const rect = el.getBoundingClientRect();
                if (rect.width < 44 || rect.height < 44) {
                    issues.push(`Alvo de toque muito pequeno (${Math.round(rect.width)}x${Math.round(rect.height)}px) em ${el.innerText.slice(0,20)}...`);
                }

                // 3. Labels
                if (el.tagName === 'BUTTON' && !el.innerText && !el.getAttribute('aria-label')) {
                    issues.push(`Botão sem label ou aria-label detectado.`);
                }
                
                // 4. Imagens sem Alt
                if (el.tagName === 'IMG' && !el.getAttribute('alt')) {
                    issues.push(`Imagem sem texto alternativo (alt).`);
                }
            });
            return issues;
        }""")

    async def fill_smartly(self, locator: Locator, tag: str, type_attr: str, name_attr: str):
        """Preenche formulários com dados realistas baseados no contexto."""
        if tag == "input":
            if type_attr == "email" or "email" in name_attr:
                await locator.fill(fake.email())
            elif type_attr == "password" or "password" in name_attr:
                await locator.fill("SenhaForte123!")
            elif type_attr == "tel" or "phone" in name_attr:
                await locator.fill(fake.phone_number())
            elif "name" in name_attr:
                await locator.fill(fake.name())
            elif type_attr == "number":
                await locator.fill(str(random.randint(1, 100)))
            elif type_attr == "text":
                await locator.fill(fake.word())
        elif tag == "textarea":
            await locator.fill(fake.sentence())

    async def generate_report(self, dirs, safe_name, route_info, elements_data, ux_issues, logs):
        """Gera o relatório Markdown ultra-detalhado."""
        report_path = dirs['docs'] / "relatorio.md"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Relatório de Inspeção Visual: {route_info['route_pattern']}\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"**URL Alvo:** `{BASE_URL}{route_info['test_url']}`\n")
            f.write(f"**Responsável:** Optimus Architect AI\n\n")

            f.write("## 1. Diagnóstico de Integridade\n")
            if logs['errors']:
                f.write("🔴 **CRÍTICO:** Erros de console detectados.\n")
            elif len(elements_data) == 0:
                f.write("🟡 **ALERTA:** Nenhum elemento interativo detectado (Página estática ou erro de renderização).\n")
            else:
                f.write("🟢 **SAUDÁVEL:** Página renderizada e interativa.\n")

            f.write("\n## 2. Evidências Visuais\n")
            f.write(f"- **Vídeo de Navegação:** [Assistir](../videos/{safe_name}.webm)\n")
            f.write(f"- **Screenshot Full Page:** [Ver Imagem](../imgs/{safe_name}_full.png)\n")

            f.write("\n## 3. Mapa de Elementos Interativos\n")
            f.write("| ID | Tipo | Texto/Label | Seletor | Ação Testada | Status |\n")
            f.write("|---|---|---|---|---|---|\n")
            
            for el in elements_data:
                status_icon = "✅" if el['status'] == "OK" else "❌"
                f.write(f"| {el['id']} | `{el['tag']}` | **{el['text']}** | `{el['selector']}` | {el['action']} | {status_icon} |\n")

            f.write("\n## 4. Análise UX/UI & Acessibilidade\n")
            if ux_issues:
                for issue in ux_issues:
                    f.write(f"- ⚠️ {issue}\n")
            else:
                f.write("- ✅ Nenhum problema óbvio de acessibilidade detectado nas heurísticas automáticas.\n")

            f.write("\n## 5. Logs do Console\n")
            if logs['errors']:
                f.write("```\n")
                for err in logs['errors']:
                    f.write(f"[ERROR] {err}\n")
                f.write("```\n")
            else:
                f.write("*Console limpo.*\n")

            f.write("\n## 6. Sugestões de Melhoria (Optimus)\n")
            f.write("- [ ] Validar se os contrastes de cor atendem WCAG AA.\n")
            f.write("- [ ] Verificar se o tempo de carregamento (LCP) está abaixo de 2.5s.\n")
            if len(elements_data) > 20:
                f.write("- [ ] **Atenção:** Alta densidade de elementos interativos. Considerar simplificar a interface.\n")

    async def process_route(self, route, browser):
        dirs, safe_name = self.setup_page_dirs(route['route_pattern'])
        url = f"{BASE_URL}{route['test_url']}"
        
        print(f"\n🔭 Iniciando inspeção profunda em: {url}")
        
        # Contexto isolado para vídeo limpo
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            record_video_dir=dirs['videos'],
            record_video_size={"width": 1280, "height": 800},
            storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None
        )
        
        # Injeção de Scripts Anti-Ruído
        await context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        
        page = await context.new_page()
        
        # Captura de Logs
        logs = {'errors': [], 'warnings': []}
        page.on("console", lambda msg: logs['errors'].append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: logs['errors'].append(str(exc)))

        try:
            # 1. Navegação e Carregamento
            await page.goto(url, wait_until="networkidle", timeout=20000)
            
            # 2. Rolagem para Vídeo e Lazy Load
            await self.smooth_scroll(page)
            
            # 3. Screenshot Full Page (Limpo)
            await page.screenshot(path=dirs['imgs'] / f"{safe_name}_full.png", full_page=True)
            
            # 4. Detecção de Elementos
            # Seletores robustos para pegar tudo que é clicável
            selectors = "button, a[href], input, select, textarea, [role='button'], div[onclick]"
            elements = await page.query_selector_all(selectors)
            
            elements_data = []
            ux_issues = await self.analyze_accessibility(page)

            print(f"   🧩 {len(elements)} elementos interativos identificados.")

            # 5. Iteração e Teste de Elementos
            for i, handle in enumerate(elements):
                if not await handle.is_visible(): continue
                
                # Dados do Elemento
                tag = await handle.evaluate("el => el.tagName.toLowerCase()")
                text = (await handle.inner_text()).strip().replace("\n", " ")[:30]
                type_attr = await handle.get_attribute("type") or ""
                name_attr = await handle.get_attribute("name") or ""
                
                # Identificador único para o relatório
                el_id = f"el_{i:03d}"
                
                # Ação: Highlight -> Print -> Interact -> Unhighlight
                await self.highlight_element(handle, color="#ea580c") # Laranja MesaFlow
                
                # Print do Elemento
                try:
                    await page.screenshot(
                        path=dirs['imgs'] / f"{safe_name}_{el_id}.png",
                        clip=await handle.bounding_box()
                    )
                except:
                    pass # Elemento pode ter movido ou estar oculto

                # Interação Realista
                action_status = "SKIPPED"
                action_desc = "Visual Only"
                
                # Lógica de Interação Segura (Não navegar se for link, apenas hover)
                if tag == "a":
                    await handle.hover()
                    action_status = "HOVERED"
                    action_desc = "Hover Link"
                elif tag in ["input", "textarea"]:
                    await self.fill_smartly(handle, tag, type_attr, name_attr)
                    action_status = "FILLED"
                    action_desc = f"Preenchido ({type_attr})"
                elif tag == "button" or tag == "div":
                    # Evitar clicar em "Sair" ou "Deletar" cegamente
                    if "sair" not in text.lower() and "excluir" not in text.lower() and "delete" not in text.lower():
                        try:
                            await handle.hover()
                            # Clicar apenas se não for navegação crítica (heurística)
                            # await handle.click(timeout=1000) 
                            action_status = "HOVERED" 
                            action_desc = "Hover/Focus"
                        except:
                            action_status = "ERROR"
                
                await page.wait_for_timeout(500) # Pausa para vídeo
                await self.unhighlight_element(handle)

                elements_data.append({
                    "id": el_id,
                    "tag": tag,
                    "text": text or "No Label",
                    "selector": f"{tag}[name='{name_attr}']" if name_attr else tag,
                    "action": action_desc,
                    "status": "OK" if action_status != "ERROR" else "FAIL"
                })

            # 6. Geração do Relatório
            await self.generate_report(dirs, safe_name, route, elements_data, ux_issues, logs)

        except Exception as e:
            print(f"   ❌ Erro crítico na página {url}: {e}")
            # Snapshot do erro
            await page.screenshot(path=dirs['imgs'] / "CRASH_REPORT.png")
            with open(dirs['docs'] / "CRASH.log", "w") as f:
                f.write(str(e))
        
        finally:
            await context.close()
            # Renomear vídeo
            video_path = await page.video().path()
            if video_path:
                try:
                    os.rename(video_path, dirs['videos'] / f"{safe_name}_navigation.webm")
                except: pass

    async def run(self):
        print("🚀 Iniciando Optimus Visual Tester v5.0")
        
        if not os.path.exists(ROUTES_FILE):
            print("❌ Arquivo de rotas não encontrado. Execute map_routes.py primeiro.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            # Launch com SlowMo para vídeos humanos
            browser = await p.chromium.launch(headless=True, slow_mo=SLOW_MO)
            
            # Login Inicial para gerar estado
            if not os.path.exists(AUTH_STATE):
                print("🔑 Gerando autenticação administrativa...")
                page = await browser.new_page()
                await page.goto(f"{BASE_URL}/admin/login")
                await page.fill('input[name="email"]', "admin@mesaflow.com")
                await page.fill('input[name="password"]', "123456")
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/dashboard", timeout=15000)
                await page.context.storage_state(path=AUTH_STATE)
                await page.close()

            # Processar cada rota
            for route in routes:
                await self.process_route(route, browser)

            await browser.close()
        
        print("\n✨ Auditoria Completa Finalizada.")
        print(f"📂 Relatórios gerados em: {OUTPUT_DIR}")

if __name__ == "__main__":
    tester = OptimusVisualTester()
    asyncio.run(tester.run())
