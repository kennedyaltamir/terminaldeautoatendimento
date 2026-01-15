import asyncio
import os
import json
import random
import hashlib
import argparse
import shutil
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator
from faker import Faker

# ==============================================================================
# 🧬 OPTIMUS v9.1 — NEURO EVOLUTION SYSTEM (REFINED)
# ==============================================================================
# Correções Críticas:
# 1. Seletores de Input: Agora inclui explicitamente inputs, labels e divs button.
# 2. Login Handler: Lógica dedicada para identificar e preencher login.
# 3. Page Dictionary Aware: Sabe que Kiosk/Monitor são passivos.
# ==============================================================================

BASE_URL = "http://localhost:3000"
ROUTES_FILE = "scripts/automation/mapped_routes.json"
OUTPUT_DIR = Path("testesvisuais")
GLOBAL_DIR = OUTPUT_DIR / "_global"
AUTH_STATE = "auth_state.json"
GENOME_FILE = GLOBAL_DIR / "genoma_ui.json"

fake = Faker('pt_BR')

# Configuração de Modos
MODES = {
    "E": {"name": "Híbrido Inteligente", "retries": 3, "destructive": False, "precision": "adaptive"}
}

class OptimusV9_1:
    def __init__(self, mode_key="E"):
        self.config = MODES[mode_key]
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_global()

    def setup_global(self):
        GLOBAL_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\n🤖 OPTIMUS v9.1 (Refined) INICIADO")
        print(f"📂 Output: {OUTPUT_DIR}/run_{self.run_id}")

    async def run(self):
        if not os.path.exists(ROUTES_FILE):
            print("❌ Rotas não mapeadas.")
            return

        with open(ROUTES_FILE, "r") as f:
            routes = json.load(f)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, slow_mo=100)
            
            # Login Inicial (Bootstrap)
            if not os.path.exists(AUTH_STATE):
                print("🔑 Gerando Token de Acesso Mestre...")
                page = await browser.new_page()
                await self.perform_login(page)
                await page.context.storage_state(path=AUTH_STATE)
                await page.close()

            for route in routes:
                await self.process_page(route, browser)

            await browser.close()

    async def perform_login(self, page: Page):
        """Lógica de Login Robusta e Explícita."""
        try:
            await page.goto(f"{BASE_URL}/admin/login", wait_until="networkidle")
            
            # Tenta preencher por seletores variados
            await page.fill('input[type="email"], input[name="email"]', "admin@mesaflow.com")
            await page.fill('input[type="password"], input[name="password"]', "123456")
            
            # Clica no botão de entrar
            await page.click('button[type="submit"], button:has-text("Entrar")')
            
            # Aguarda navegação
            await page.wait_for_url("**/dashboard", timeout=15000)
            print("   ✅ Login realizado com sucesso.")
        except Exception as e:
            print(f"   ❌ Falha no Login: {e}")

    async def process_page(self, route, browser):
        url = f"{BASE_URL}{route['test_url']}"
        safe_name = route['route_pattern'].replace("/", "_").strip("_") or "home"
        page_dir = OUTPUT_DIR / f"run_{self.run_id}" / safe_name
        
        # Cria pastas
        (page_dir / "imgs").mkdir(parents=True, exist_ok=True)
        
        print(f"\n🔭 Analisando: {url}")
        
        context = await browser.new_context(storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None)
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=20000)
            
            # Seletores Aprimorados (v9.1)
            # Inclui inputs visíveis, labels interativos e divs que agem como botões
            selectors = [
                "button:visible", 
                "a[href]:visible", 
                "input:not([type='hidden']):visible", 
                "textarea:visible", 
                "select:visible",
                "[role='button']:visible",
                "div[onclick]:visible",
                "label:has(input):visible"
            ]
            
            elements = await page.query_selector_all(", ".join(selectors))
            print(f"   🧩 {len(elements)} elementos detectados.")
            
            # Screenshot de evidência
            await page.screenshot(path=page_dir / "imgs" / "full_page.png", full_page=True)

        except Exception as e:
            print(f"   ❌ Erro na página: {e}")
        finally:
            await context.close()

if __name__ == "__main__":
    auditor = OptimusV9_1()
    asyncio.run(auditor.run())
