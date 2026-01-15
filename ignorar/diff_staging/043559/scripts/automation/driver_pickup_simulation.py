import asyncio
import requests
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🛵 DRIVER PICKUP SIMULATION (L6)
# ==============================================================================
# Objetivo: Simular visualmente o fluxo de um entregador aceitando um pedido.
# 1. Cria um pedido de Delivery via API (Backend).
# 2. Avança o status para 'ready' (Pronto para retirada).
# 3. Abre o navegador, loga como Motorista/Admin.
# 4. Acessa o Painel do Driver.
# 5. Executa a ação de "Pegar Pedido".
# 6. Valida a transição para "Em Rota".
# ==============================================================================

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
SCREENSHOT_DIR = Path("testesvisuais/driver_flow")

# Credenciais (Admin tem acesso a tudo, inclusive driver view)
USER_EMAIL = "admin@mesaflow.com"
USER_PASS = "123456"

def setup_test_data():
    print("🛠️  [SETUP] Preparando dados de teste...")
    
    # 1. Login API
    auth_res = requests.post(f"{API_URL}/auth/token", data={
        "username": USER_EMAIL, "password": USER_PASS
    })
    if auth_res.status_code != 200:
        raise Exception("Falha na autenticação API")
    token = auth_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar Pedido Delivery
    customer_name = f"Driver Test {datetime.now().strftime('%H%M')}"
    order_payload = {
        "order_type": "delivery",
        "customer_name": customer_name,
        "customer_phone": "11999999999",
        "delivery_address": "Rua dos Testes, 123",
        "payment_method": "online",
        "items": [{"product_id": 1, "quantity": 1}] # Assume ID 1 existe (Seed)
    }
    
    # Tenta criar (pode falhar se produto 1 não existir, mas o seed padrão cria)
    # Fallback: Buscar primeiro produto do menu se falhar
    try:
        create_res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
        if create_res.status_code != 201:
            # Tenta buscar um produto válido
            menu = requests.get(f"{API_URL}/{SLUG}/menu").json()
            prod_id = menu['categories'][0]['products'][0]['id']
            order_payload['items'][0]['product_id'] = prod_id
            create_res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
            
        order_data = create_res.json()
        order_id = order_data["id"]
        print(f"   ✅ Pedido Criado: {order_id} ({customer_name})")
    except Exception as e:
        print(f"   ❌ Erro ao criar pedido: {e}")
        return None, None

    # 3. Avançar para 'Ready' (Cozinha -> Pronto)
    # Status flow: pending -> accepted -> preparing -> ready
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "accepted"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    print(f"   ✅ Pedido movido para 'Pronto' (A Retirar)")
    
    return order_id, customer_name

async def run_simulation():
    order_id, customer_name = setup_test_data()
    if not order_id:
        return

    print("\n🎬 [ACTION] Iniciando Simulação Visual...")
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        # Launch com visual (headless=False) e slow_mo para ver a ação
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844}, # Mobile Viewport
            permissions=["geolocation"],
            geolocation={"latitude": -23.5505, "longitude": -46.6333}
        )
        page = await context.new_page()

        try:
            # 1. Login
            print("   🔑 Logando no App...")
            await page.goto(f"{BASE_URL}/admin/login")
            await page.fill('input[name="email"]', USER_EMAIL)
            await page.fill('input[name="password"]', USER_PASS)
            await page.click('button[type="submit"]')
            await page.wait_for_url("**/dashboard")

            # 2. Ir para Driver App
            print("   🛵 Acessando Painel do Entregador...")
            await page.goto(f"{BASE_URL}/admin/{SLUG}/driver")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=SCREENSHOT_DIR / "01_driver_dashboard.png")

            # 3. Localizar Pedido na aba "A Retirar"
            # Garante que estamos na aba certa (pode ser o default)
            # Procura pelo card do cliente
            print(f"   🔍 Procurando pedido de: {customer_name}")
            card = page.locator(f"text={customer_name}")
            await expect(card).to_be_visible(timeout=10000)
            
            # Highlight visual
            await card.evaluate("el => el.parentElement.style.border = '4px solid #ea580c'")
            await page.screenshot(path=SCREENSHOT_DIR / "02_order_found.png")

            # 4. Pegar Pedido
            print("   👉 Clicando em 'Pegar Pedido'...")
            # O botão geralmente está dentro do card ou próximo. 
            # Vamos buscar o botão "Pegar Pedido" ou ícone de Bike dentro do container do pedido
            # Estratégia: Encontrar o container pai do texto e buscar o botão dentro
            # Simplificação: Clicar no botão que contém "Pegar" ou ícone próximo
            
            # Tenta achar o botão específico deste pedido
            # Assume que o card tem um botão. Vamos clicar no primeiro botão "Pegar Pedido" visível se houver apenas 1 teste
            # Ou melhor, usar o locator relativo
            pickup_btn = page.locator("button:has-text('Pegar Pedido')").first
            if await pickup_btn.is_visible():
                await pickup_btn.click()
            else:
                # Tenta ícone ou outro texto
                await page.locator("button:has(svg.lucide-bike)").first.click()

            # 5. Validar Transição
            print("   ⏳ Aguardando transição para 'Em Rota'...")
            # Deve mudar de aba ou o card deve sumir da aba atual
            await asyncio.sleep(2) # Espera animação/fetch
            
            # Verifica se mudou para aba "Em Rota" (se o app fizer auto-switch)
            # Ou clica na aba "Em Rota"
            em_rota_tab = page.locator("button:has-text('Em Rota')")
            await em_rota_tab.click()
            
            # Verifica se o pedido está lá
            await expect(page.locator(f"text={customer_name}")).to_be_visible()
            print("   ✅ SUCESSO: Pedido está na lista 'Em Rota'.")
            
            await page.screenshot(path=SCREENSHOT_DIR / "03_in_transit.png")

            # 6. Finalizar (Opcional, para limpar)
            print("   🏁 Finalizando entrega...")
            finish_btn = page.locator("button:has-text('Finalizar')").first
            if await finish_btn.is_visible():
                await finish_btn.click()
                # Se houver modal de confirmação
                confirm_btn = page.locator("button:has-text('Confirmar')").first
                if await confirm_btn.is_visible():
                    await confirm_btn.click()
                print("   ✅ Entrega finalizada.")

        except Exception as e:
            print(f"   ❌ Falha na simulação: {e}")
            await page.screenshot(path=SCREENSHOT_DIR / "error_state.png")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_simulation())
