import asyncio
import requests
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🛵 REAL-TIME DELIVERY & TRACKING SIMULATION (L6)
# ==============================================================================
# Objetivo: Simular a sincronia entre o Entregador e o Cliente Final.
# 1. Cria um pedido de Delivery.
# 2. Abre duas janelas: [Motorista] e [Cliente].
# 3. Motorista clica em "Pegar Pedido".
# 4. Valida se o Cliente recebe o status "Motorista a caminho" via WebSocket.
# 5. Simula o movimento do motorista (GPS).
# ==============================================================================

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
SCREENSHOT_DIR = Path("testesvisuais/realtime_delivery")

# Credenciais
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def setup_order():
    print("🛠️  [1/5] Criando pedido de delivery via API...")
    order_payload = {
        "order_type": "delivery",
        "customer_name": f"Cliente Realtime {datetime.now().strftime('%H%M')}",
        "customer_phone": "11988887777",
        "delivery_address": "Av. Paulista, 1000, São Paulo",
        "payment_method": "online",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    
    # Tenta criar o pedido
    res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    if res.status_code != 201:
        # Fallback para produto dinâmico
        menu = requests.get(f"{API_URL}/{SLUG}/menu").json()
        order_payload['items'][0]['product_id'] = menu['categories'][0]['products'][0]['id']
        res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    
    order = res.json()
    order_id = order["id"]
    
    # Login para avançar status
    auth = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
    headers = {"Authorization": f"Bearer {auth['access_token']}"}
    
    # Move para READY (Pronto para Retirada)
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    print(f"   ✅ Pedido {order_id[:8]} pronto para retirada.")
    return order_id, order_payload['customer_name']

async def run_simulation():
    order_id, customer_name = await setup_order()
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        
        # --- CONTEXTO DO MOTORISTA ---
        print("\n📱 [2/5] Abrindo Painel do Entregador...")
        driver_context = await browser.new_context(
            viewport={"width": 400, "height": 800},
            permissions=["geolocation"],
            geolocation={"latitude": -23.5505, "longitude": -46.6333}
        )
        driver_page = await driver_context.new_page()
        
        # Login Driver
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill('input[name="email"]', ADMIN_EMAIL)
        await driver_page.fill('input[name="password"]', ADMIN_PASS)
        await driver_page.click('button[type="submit"]')
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # --- CONTEXTO DO CLIENTE ---
        print("👤 [3/5] Abrindo Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 400, "height": 800})
        customer_page = await customer_context.new_page()
        # Acessa a URL de acompanhamento do pedido
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        await customer_page.wait_for_load_state("networkidle")
        
        # Valida estado inicial do cliente (Pronto)
        await expect(customer_page.locator("text=Pronto")).to_be_visible()
        print("   ✅ Cliente visualiza: 'Pedido Pronto'.")

        # --- AÇÃO: MOTORISTA PEGA O PEDIDO ---
        print("\n👉 [4/5] Motorista clicando em 'Pegar Pedido'...")
        pickup_btn = driver_page.locator(f"div:has-text('{customer_name}') >> button:has-text('Pegar')").first
        await pickup_btn.evaluate("el => el.style.border = '4px solid #ea580c'")
        await pickup_btn.click()
        
        # --- VALIDAÇÃO REAL-TIME NO CLIENTE ---
        print("⏳ [5/5] Validando atualização automática no Cliente...")
        # O cliente deve mudar para "Em Rota" ou "Motorista a caminho" via WebSocket
        await expect(customer_page.locator("text=Em Rota")).to_be_visible(timeout=10000)
        await customer_page.screenshot(path=SCREENSHOT_DIR / "customer_en_route.png")
        print("   ✨ SUCESSO: Cliente recebeu atualização 'Em Rota' em tempo real!")

        # Simula movimento (Opcional: se o app tiver lógica de watchPosition)
        print("\n📍 Simulando deslocamento do entregador...")
        await driver_context.set_geolocation({"latitude": -23.5515, "longitude": -46.6343})
        await asyncio.sleep(2)
        
        print("\n🏁 Simulação concluída com sucesso.")
        await asyncio.sleep(2)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_simulation())
