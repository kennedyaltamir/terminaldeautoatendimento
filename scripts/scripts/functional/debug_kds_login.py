import os
import time
from playwright.sync_api import sync_playwright

# Configurações
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
TARGET_URL = f"{BASE_URL}/admin/{SLUG}/kitchen"
SCREENSHOT_DIR = "debug_screenshots"

def run_debug():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    print(f"🕵️ Iniciando Diagnóstico Visual em: {TARGET_URL}")

    with sync_playwright() as p:
        # Abre o navegador visível (headless=False) para você ver acontecer
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        
        # 1. Injetar Token ANTES de carregar a página
        print("💉 Injetando Token Fake...")
        context.add_init_script("""
            localStorage.setItem('mesaflow_access_token', 'fake-jwt-token-debug');
            localStorage.setItem('mesaflow_user_role', 'kitchen');
            console.log('Token injetado pelo script de debug');
        """)

        page = context.new_page()

        # Capturar logs do console do navegador
        page.on("console", lambda msg: print(f"   [BROWSER CONSOLE] {msg.text}"))
        page.on("pageerror", lambda exc: print(f"   [BROWSER ERROR] {exc}"))

        # 2. Tentar acessar o KDS
        print(f"🚀 Navegando para {TARGET_URL}...")
        try:
            page.goto(TARGET_URL)
            page.screenshot(path=f"{SCREENSHOT_DIR}/01_after_nav.png")
            
            # Esperar um pouco para ver se redireciona
            print("⏳ Aguardando 5 segundos para verificar redirecionamento...")
            time.sleep(5)
            
            current_url = page.url
            print(f"📍 URL Atual: {current_url}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/02_final_state.png")

            if "/login" in current_url:
                print("❌ FALHA: O sistema redirecionou para o Login.")
                print("   Causa provável: O frontend tentou validar o token no backend e recebeu 401.")
            elif "/kitchen" in current_url:
                print("✅ SUCESSO: O sistema permaneceu no KDS.")
                
                # Tentar achar o botão
                print("🔍 Procurando botão 'Resumo de Produção'...")
                try:
                    btn = page.locator('button[title="Resumo de Produção"]')
                    if btn.is_visible():
                        print("✅ Botão ENCONTRADO!")
                        btn.click()
                        page.screenshot(path=f"{SCREENSHOT_DIR}/03_modal_open.png")
                    else:
                        print("❌ Botão NÃO visível na tela.")
                except Exception as e:
                    print(f"❌ Erro ao buscar botão: {e}")

        except Exception as e:
            print(f"🔥 Erro Crítico: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/99_error.png")
        
        finally:
            browser.close()
            print(f"\n📸 Prints salvos na pasta '{SCREENSHOT_DIR}'")

if __name__ == "__main__":
    # Verifica se playwright está instalado
    try:
        import playwright
        run_debug()
    except ImportError:
        print("❌ Playwright Python não instalado.")
        print("👉 Rode: pip install playwright && playwright install chromium")
