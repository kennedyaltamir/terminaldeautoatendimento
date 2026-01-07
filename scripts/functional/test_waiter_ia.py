import os
import time
import json
from playwright.sync_api import sync_playwright

# Configurações
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
TABLE_ID = "1"
TARGET_URL = f"{BASE_URL}/admin/{SLUG}/waiter/pos/{TABLE_ID}"
SCREENSHOT_DIR = "debug_screenshots"

def run_test():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    print(f"🕵️ INICIANDO TESTE FUNCIONAL: IA UPSELLING NO POS")
    print(f"🎯 Alvo: {TARGET_URL}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )

        # 1. INJEÇÃO DE AUTH
        context.add_init_script("""
            localStorage.setItem('mesaflow_access_token', 'fake-jwt-token-python');
            localStorage.setItem('mesaflow_user_role', 'cashier');
            localStorage.setItem('mesaflow_tour_completed', 'true');
        """)

        page = context.new_page()

        # --- MOCKS DE API ---
        print("🛡️ Configurando Mocks de API...")

        # Mock Menu com Recomendações e option_groups vazio
        page.route(f"**/api/{SLUG}/menu", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "company": { "name": "Bar do Zé", "segment": "gastro" },
                "categories": [{
                    "id": 1, 
                    "name": "Lanches", 
                    "products": [
                        { 
                            "id": 1, 
                            "name": "X-Burger", 
                            "price": 20.00, 
                            "option_groups": [], # CORREÇÃO: Campo obrigatório
                            "recommendations": [
                                { "id": 2, "name": "Batata Frita", "price": 10.00, "option_groups": [] }
                            ]
                        },
                        { "id": 2, "name": "Batata Frita", "price": 10.00, "option_groups": [] }
                    ]
                }]
            })
        ))

        # Mocks Auxiliares
        page.route("**/api/admin/company/me", lambda route: route.fulfill(status=200, body=json.dumps({"name": "Bar do Zé"})))
        page.route(f"**/api/{SLUG}/check-table", lambda route: route.fulfill(status=200, body=json.dumps({"status": "active", "session_token": "sess-123", "customer_name": "Cliente IA"})))
        page.route(f"**/api/{SLUG}/session/sess-123", lambda route: route.fulfill(status=200, body=json.dumps({"id": 123, "customer_name": "Cliente IA", "total_spent": 0, "orders": []})))
        page.route("**/api/admin/metrics*", lambda route: route.fulfill(status=200, body=json.dumps({"top_products": []})))

        # --- EXECUÇÃO ---
        try:
            print(f"🚀 Navegando para {TARGET_URL}...")
            page.goto(TARGET_URL, wait_until="domcontentloaded")
            
            print("✅ Página carregada.")
            
            # 1. Adicionar X-Burger
            print("🖱️ Adicionando X-Burger...")
            page.get_by_text("X-Burger").click()
            
            # 2. Verificar Sugestão
            print("👀 Aguardando Sugestão da IA...")
            suggestion = page.locator("text=Sugestão da IA")
            suggestion.wait_for(state="visible", timeout=5000)
            
            print("✅ Toast de Sugestão apareceu!")
            page.screenshot(path=f"{SCREENSHOT_DIR}/ia_suggestion_visible.png")
            
            # 3. Aceitar Sugestão
            print("🖱️ Aceitando sugestão (Batata Frita)...")
            page.get_by_role("button", name="Adicionar").click()
            
            # 4. Verificar Carrinho
            print("🛒 Verificando carrinho...")
            cart_count = page.locator("text=2 itens")
            cart_count.wait_for(state="visible", timeout=2000)
            
            print("🎉 SUCESSO: Item sugerido adicionado ao carrinho!")
            page.screenshot(path=f"{SCREENSHOT_DIR}/ia_success.png")

        except Exception as e:
            print(f"🔥 ERRO NO TESTE: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/ia_error.png")
        
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()
