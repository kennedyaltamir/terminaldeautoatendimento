import os
import time
import json
from playwright.sync_api import sync_playwright

# Configurações
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
TARGET_URL = f"{BASE_URL}/admin/{SLUG}/settings"
SCREENSHOT_DIR = "debug_screenshots"

def verify_ui():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    print(f"🕵️ Iniciando Verificação Visual: Configuração de Impressora")

    with sync_playwright() as p:
        # Headless=False para você ver acontecendo
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # 1. Injetar Token de Dono E pular o Tour
        context.add_init_script("""
            localStorage.setItem('mesaflow_access_token', 'fake-jwt-token-visual-check');
            localStorage.setItem('mesaflow_user_role', 'owner');
            localStorage.setItem('mesaflow_tour_completed', 'true'); // <--- PULA O TOUR
        """)

        page = context.new_page()

        # 2. Mock da API de Perfil (Evita 401 e Redirect para Login)
        page.route("**/api/admin/company/me", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "name": "Hamburgueria Visual Test",
                "plan_tier": "pro",
                "owner_email": "admin@teste.com",
                "primary_color": "#ea580c"
            })
        ))

        try:
            print(f"🚀 Navegando para {TARGET_URL}...")
            page.goto(TARGET_URL)
            
            # Aguarda carregamento inicial
            page.wait_for_selector("text=Configurações", timeout=10000)
            
            print("🖱️ Clicando na aba 'Impressão'...")
            # Clica na aba
            page.get_by_text("Impressão").click()
            
            # Aguarda o componente aparecer
            page.wait_for_selector("text=Configuração de Impressão (App)")
            
            # Pequeno delay para animação
            time.sleep(1)
            
            # Screenshot
            path = f"{SCREENSHOT_DIR}/printer_settings_success.png"
            page.screenshot(path=path)
            print(f"✅ Sucesso! Screenshot salvo em: {path}")
            
            # Verifica se os botões de 58mm/80mm estão lá
            if page.get_by_text("58mm (Padrão)").is_visible():
                print("   [OK] Opção 58mm visível")
            if page.get_by_text("80mm (Largo)").is_visible():
                print("   [OK] Opção 80mm visível")

        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/printer_settings_error.png")
        
        finally:
            browser.close()

if __name__ == "__main__":
    verify_ui()
