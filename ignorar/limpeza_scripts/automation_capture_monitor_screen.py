# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 15:30:00
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

# Configurações
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
OUTPUT_PATH = Path("docs/screenshots/public_monitor_v3.png")

async def capture_monitor():
    print(f"📸 Capturando interface do Monitor Público para {SLUG}")
    
    if not OUTPUT_PATH.parent.exists():
        OUTPUT_PATH.parent.mkdir(parents=True)

    async with async_playwright() as p:
        # Lançar navegador (Headless para automação)
        browser = await p.chromium.launch()
        
        # Configurar viewport para TV Full HD
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        url = f"{BASE_URL}/{SLUG}/monitor"
        
        try:
            print(f"🌐 Navegando para {url}")
            await page.goto(url, wait_until="networkidle", timeout=15000)
            
            # Aguarda animações do Framer Motion estabilizarem
            await asyncio.sleep(2)
            
            # Tira o print
            await page.screenshot(path=str(OUTPUT_PATH))
            print(f"✅ Screenshot salva com sucesso em: {OUTPUT_PATH}")
            
        except Exception as e:
            print(f"❌ Erro ao capturar tela: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_monitor())
