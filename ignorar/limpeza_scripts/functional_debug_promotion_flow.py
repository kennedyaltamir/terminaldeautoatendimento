import os
import time
import json
from playwright.sync_api import sync_playwright

# Configurações
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
TARGET_URL = f"{BASE_URL}/{SLUG}/menu"
SCREENSHOT_DIR = "debug_screenshots"

def run_debug():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    print(f"🕵️ Iniciando Diagnóstico Visual: Fluxo de Promoção")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        # 1. Mock do Menu (Para garantir que o produto existe e tem tags)
        mock_menu = {
            "company": {
                "name": "Loja Debug",
                "is_active": True,
                "primary_color": "#ea580c",
                "currency": "BRL"
            },
            "categories": [
                {
                    "id": 1,
                    "name": "Lanches",
                    "products": [
                        {
                            "id": 100,
                            "name": "Hambúrguer Debug",
                            "price": 50.00,
                            "is_available": True,
                            "track_stock": False,
                            "option_groups": [],
                            "tags": ["promo", "debug"] # Importante para não quebrar
                        }
                    ]
                }
            ]
        }

        page.route("**/api/*/menu", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_menu)
        ))

        try:
            print(f"🚀 Navegando para {TARGET_URL}...")
            page.goto(TARGET_URL)
            page.wait_for_timeout(2000)
            page.screenshot(path=f"{SCREENSHOT_DIR}/01_menu_loaded.png")

            # 2. Adicionar ao Carrinho
            print("🛒 Adicionando produto...")
            page.get_by_text("Hambúrguer Debug").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Adicionar").click()
            page.screenshot(path=f"{SCREENSHOT_DIR}/02_added_to_cart.png")

            # 3. Abrir Carrinho
            print("📂 Abrindo carrinho...")
            page.get_by_role("button", name="Ver Carrinho").click()
            page.wait_for_timeout(1000)
            page.screenshot(path=f"{SCREENSHOT_DIR}/03_cart_open.png")

            # 4. Verificar Campo de Cupom
            print("🔍 Verificando campo de cupom...")
            coupon_input = page.get_by_placeholder("CÓDIGO")
            if coupon_input.is_visible():
                print("✅ Campo de cupom visível.")
                coupon_input.fill("TESTE10")
                page.screenshot(path=f"{SCREENSHOT_DIR}/04_coupon_filled.png")
            else:
                print("❌ Campo de cupom NÃO encontrado.")

        except Exception as e:
            print(f"🔥 Erro no script: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/99_error.png")

        finally:
            browser.close()
            print(f"\n📸 Prints salvos em '{SCREENSHOT_DIR}'")

if __name__ == "__main__":
    run_debug()
