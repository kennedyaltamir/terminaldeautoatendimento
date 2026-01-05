import os
import time
import json
from playwright.sync_api import sync_playwright

# Configurações
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
ORDER_ID = "order-123"
TARGET_URL = f"{BASE_URL}/{SLUG}/menu"
SCREENSHOT_DIR = "debug_screenshots"

def run_debug():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    print(f"🕵️ Iniciando Diagnóstico Visual Avançado: Fluxo de Feedback")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        
        # 1. Injetar ID do Pedido no LocalStorage
        context.add_init_script(f"""
            localStorage.setItem('mesaflow_active_order', '{ORDER_ID}');
        """)

        page = context.new_page()

        # --- MONITORES DE DIAGNÓSTICO ---
        
        # Monitor de Console
        page.on("console", lambda msg: print(f"   [JS CONSOLE] {msg.text}"))
        
        # Monitor de Rede (Para ver se o Mock funcionou)
        page.on("request", lambda request: print(f"   >> [REQ] {request.method} {request.url}") if "api" in request.url else None)
        page.on("response", lambda response: print(f"   << [RES] {response.status} {response.url}") if "api" in response.url else None)

        # 2. MOCK DA API DE PEDIDO
        mock_order = {
            "id": ORDER_ID,
            "status": "delivered",
            "payment_status": "paid",
            "total_amount": 50.00,
            "customer_name": "Cliente Debug",
            "items": [
                {
                    "id": 1,
                    "quantity": 1, 
                    "product": { "name": "X-Bacon Debug", "price": 50.00, "image_url": None }, 
                    "selected_options": [] 
                }
            ],
            "feedback": None,
            "company": { "slug": SLUG },
            "created_at": "2023-01-01T12:00:00Z",
            "payment_method": "online",
            "order_type": "delivery",
            "mp_qr_code": None
        }

        # Mock estrito para garantir que a URL bata
        page.route(f"**/api/orders/{ORDER_ID}", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_order)
        ))

        try:
            print(f"🚀 Navegando para {TARGET_URL}...")
            page.goto(TARGET_URL)
            
            # Espera inicial
            page.wait_for_timeout(3000)
            
            # Diagnóstico de Estado
            print("\n--- ANÁLISE DE ESTADO ---")
            
            # 1. Verificar LocalStorage
            ls_order = page.evaluate("localStorage.getItem('mesaflow_active_order')")
            print(f"💾 LocalStorage 'mesaflow_active_order': {ls_order}")

            # 2. Verificar em qual tela estamos
            is_status_view = page.get_by_text("Olá, Cliente!").is_visible()
            is_menu_view = page.get_by_text("Rápidos").is_visible() or page.get_by_text("Lanches").is_visible()

            if is_status_view:
                print("✅ Estamos na TELA DE STATUS (Correto).")
            elif is_menu_view:
                print("❌ Estamos na TELA DE CARDÁPIO (Errado - O pedido não foi carregado).")
            else:
                print("⚠️ Estamos em uma tela desconhecida ou carregando.")

            page.screenshot(path=f"{SCREENSHOT_DIR}/debug_state.png")

            # 3. Procurar o botão se estivermos na tela certa
            if is_status_view:
                print("🔍 Procurando botão 'Avaliar Pedido'...")
                
                # Scroll até o fim
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

                btn = page.get_by_test_id("btn-avaliar")
                if btn.is_visible():
                    print("🎉 Botão ENCONTRADO e VISÍVEL!")
                    btn.click()
                    page.wait_for_timeout(1000)
                    page.screenshot(path=f"{SCREENSHOT_DIR}/debug_success.png")
                else:
                    print("❌ Botão NÃO visível.")
                    # Debug do HTML
                    html = page.content()
                    if "btn-avaliar" in html:
                        print("   ⚠️ O elemento existe no HTML mas está oculto (CSS/Display).")
                    else:
                        print("   ⚠️ O elemento NÃO foi renderizado no HTML.")

        except Exception as e:
            print(f"🔥 Erro no script: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/debug_crash.png")
        
        finally:
            browser.close()
            print(f"\n📸 Prints salvos em '{SCREENSHOT_DIR}'")

if __name__ == "__main__":
    run_debug()
