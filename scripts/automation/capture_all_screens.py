# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 02:40:00
import asyncio
import os
from playwright.async_api import async_playwright
from pathlib import Path

# Configurações
BASE_URL = "http://localhost:3000"
DEFAULT_SLUG = "hamburgueria-ze"
OUTPUT_DIR = Path("docs/screenshots")
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

ROUTES = [
    {"name": "01_Landing", "path": "/"},
    {"name": "02_Login", "path": "/admin/login"},
    {"name": "03_Register", "path": "/admin/register"},
    {"name": "04_Menu_Publico", "path": f"/{DEFAULT_SLUG}/menu"},
    {"name": "05_Kiosk", "path": f"/{DEFAULT_SLUG}/kiosk"},
    {"name": "06_Dashboard", "path": f"/admin/{DEFAULT_SLUG}/dashboard"},
    {"name": "07_KDS", "path": f"/admin/{DEFAULT_SLUG}/kitchen"},
    {"name": "08_Waiter", "path": f"/admin/{DEFAULT_SLUG}/waiter"},
    {"name": "09_Delivery", "path": f"/admin/{DEFAULT_SLUG}/delivery"},
    {"name": "10_Inventory", "path": f"/admin/{DEFAULT_SLUG}/inventory"},
    {"name": "11_Tables", "path": f"/admin/{DEFAULT_SLUG}/tables"},
    {"name": "12_Settings", "path": f"/admin/{DEFAULT_SLUG}/settings"},
    {"name": "13_Franchise", "path": f"/admin/{DEFAULT_SLUG}/franchise"},
    {"name": "14_Audit", "path": f"/admin/{DEFAULT_SLUG}/audit"},
    {"name": "15_Trust_Status", "path": "/trust/status"},
]

async def capture():
    print("📸 Iniciando Auditoria Visual MesaFlow")
    
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True)

    async with async_playwright() as p:
        # Lançar navegador
        browser = await p.chromium.launch(headless=True)
        
        # 1. Fluxo de Login para obter estado autenticado
        print("🔑 Realizando login administrativo")
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/admin/login")
        await page.fill('input[name="email"]', ADMIN_EMAIL)
        await page.fill('input[name="password"]', ADMIN_PASS)
        await page.click('button[type="submit"]')
        await page.wait_for_url("**/dashboard")
        
        # Salva o estado de autenticação (cookies/localStorage)
        storage = await context.storage_state()
        await context.close()

        # 2. Capturar Telas
        for route in ROUTES:
            name = route["name"]
            path = route["path"]
            url = f"{BASE_URL}{path}"
            
            print(f"🖼️  Capturando: {name}")

            # --- DESKTOP ---
            ctx_desktop = await browser.new_context(storage_state=storage, viewport={'width': 1280, 'height': 800})
            p_desktop = await ctx_desktop.new_page()
            try:
                await p_desktop.goto(url, wait_until="networkidle", timeout=15000)
                await asyncio.sleep(1) # Estabilização de animações
                await p_desktop.screenshot(path=OUTPUT_DIR / f"{name}_desktop.png", full_page=False)
            except Exception as e:
                print(f"⚠️ Falha desktop {name}: {e}")
            await ctx_desktop.close()

            # --- MOBILE ---
            ctx_mobile = await browser.new_context(
                storage_state=storage, 
                viewport={'width': 390, 'height': 844},
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
            )
            p_mobile = await ctx_mobile.new_page()
            try:
                await p_mobile.goto(url, wait_until="networkidle", timeout=15000)
                await asyncio.sleep(1)
                await p_mobile.screenshot(path=OUTPUT_DIR / f"{name}_mobile.png", full_page=False)
            except Exception as e:
                print(f"⚠️ Falha mobile {name}: {e}")
            await ctx_mobile.close()

        await browser.close()
        print(f"\n✅ Auditoria concluída! {len(os.listdir(OUTPUT_DIR))} imagens salvas em '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    asyncio.run(capture())
