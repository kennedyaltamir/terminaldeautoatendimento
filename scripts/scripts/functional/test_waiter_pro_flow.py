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

    print(f"🕵️ INICIANDO TESTE FUNCIONAL: GARÇOM PRO (Python)")
    print(f"🎯 Alvo: {TARGET_URL}")

    with sync_playwright() as p:
        # headless=False para você ver o navegador abrindo
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )

        # 1. INJEÇÃO DE AUTH
        print("💉 Injetando Tokens de Autenticação...")
        context.add_init_script("""
            localStorage.setItem('mesaflow_access_token', 'fake-jwt-token-python');
            localStorage.setItem('mesaflow_user_role', 'cashier');
            localStorage.setItem('mesaflow_tour_completed', 'true');
        """)

        page = context.new_page()

        # --- MOCKS DE API ---
        print("🛡️ Configurando Mocks de API...")

        page.route("**/api/admin/company/me", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "name": "Bar do Zé",
                "plan_tier": "pro",
                "service_fee_percentage": 10.00,
                "owner_email": "admin@teste.com"
            })
        ))

        page.route(f"**/api/{SLUG}/check-table", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "status": "active",
                "session_token": "sess-python-123",
                "customer_name": "Cliente Python"
            })
        ))

        page.route(f"**/api/{SLUG}/session/sess-python-123", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "id": 123,
                "customer_name": "Cliente Python",
                "total_spent": 100.00,
                "orders": [
                    {
                        "id": "ord-1",
                        "total_amount": 100.00,
                        "status": "delivered",
                        "items": [{"product": {"name": "Picanha", "price": 100.00}, "quantity": 1, "selected_options": []}]
                    }
                ]
            })
        ))

        page.route(f"**/api/{SLUG}/menu", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "company": { "name": "Bar do Zé", "segment": "gastro" },
                "categories": []
            })
        ))

        page.route("**/api/admin/metrics*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"top_products": []})
        ))

        def handle_close(route):
            # CORREÇÃO: route.request é uma propriedade, não um método
            try:
                raw_data = route.request.post_data
                data = json.loads(raw_data) if raw_data else {}
                
                print(f"   📤 Payload Recebido: {data}")

                if data.get("custom_service_fee") == 15:
                    route.fulfill(status=200, body=json.dumps({"message": "Mesa fechada"}))
                else:
                    print(f"   ❌ ERRO: Gorjeta esperada 15, recebida {data.get('custom_service_fee')}")
                    route.fulfill(status=400, body=json.dumps({"detail": "Gorjeta incorreta"}))
            except Exception as e:
                print(f"   🔥 Erro no handler: {e}")
                route.abort()

        page.route(f"**/api/admin/tables/{TABLE_ID}/close", handle_close)

        # --- EXECUÇÃO ---
        try:
            print(f"🚀 Navegando para {TARGET_URL}...")
            page.goto(TARGET_URL, wait_until="domcontentloaded")
            
            time.sleep(2)
            if "/login" in page.url:
                print("❌ FALHA CRÍTICA: Redirecionado para Login!")
                return

            print("✅ Página carregada.")
            
            # 1. Abrir Modal
            print("🖱️ Clicando em 'Fechar Conta'...")
            try:
                btn_close = page.locator('button[title="Fechar Conta"]')
                btn_close.wait_for(state="visible", timeout=10000)
                btn_close.click(force=True)
            except:
                 print("⚠️ Botão não encontrado pelo título. Tentando seletor genérico...")
                 btn_close = page.locator('button.bg-green-600')
                 btn_close.click(force=True)
            
            # 2. Validar Modal Aberto
            print("👀 Verificando Modal...")
            page.wait_for_selector("text=TOTAL FINAL", timeout=10000)
            
            # 3. Editar Gorjeta
            print("✏️ Procurando botão de editar gorjeta...")
            
            edit_buttons = page.locator("button svg.lucide-edit-2")
            count = edit_buttons.count()
            
            clicked = False
            if count > 0:
                for i in range(count):
                    btn = edit_buttons.nth(i).locator("..")
                    if btn.is_visible():
                        btn.click()
                        clicked = True
                        break
            
            if not clicked:
                print("⚠️ Tentando via texto 'Serviço'...")
                container = page.locator("div").filter(has_text="Serviço").last
                container.locator("button").click()

            # Digita 15%
            print("⌨️ Digitando 15%...")
            tip_input = page.locator('input[type="number"]').first
            tip_input.wait_for(state="visible", timeout=2000)
            tip_input.fill("15")
            
            # Verifica se o total mudou (100 + 15 = 115)
            print("🧮 Verificando recálculo...")
            page.wait_for_selector("text=115.00", timeout=5000)
            print("✅ Total atualizado para R$ 115.00")

            # 4. Finalizar
            print("💰 Selecionando Dinheiro...")
            page.get_by_text("Dinheiro").click()
            
            print("✅ Calculadora de Troco visível.")
            
            # Digitar valor na calculadora
            print("⌨️ Digitando valor recebido (120)...")
            page.get_by_role("button", name="1", exact=True).click()
            page.get_by_role("button", name="2", exact=True).click()
            page.get_by_role("button", name="0", exact=True).click()
            
            # Simula pagamento
            print("🖱️ Confirmando Pagamento...")
            page.get_by_text("Confirmar Pagamento").click()
            
            # 5. Sucesso
            page.wait_for_selector("text=Mesa finalizada", timeout=5000)
            print("🎉 SUCESSO: Fluxo de Garçom Pro validado!")
            
            page.screenshot(path=f"{SCREENSHOT_DIR}/success_waiter_pro.png")

        except Exception as e:
            print(f"🔥 ERRO NO TESTE: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/error_state.png")
        
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()
