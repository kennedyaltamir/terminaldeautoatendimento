# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 08:55:00
import asyncio
import requests
import json
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🛵 REAL-TIME DELIVERY & TRACKING SIMULATION (L6.3 - Anti-Interception)
# ==============================================================================
# Objetivo: Simular a sincronia entre o Entregador e o Cliente Final.
# Fix v6.3: Injeção de LocalStorage para desativar Onboarding Tour (Joyride).
# ==============================================================================

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
SCREENSHOT_DIR = Path("testesvisuais/realtime_delivery")
GLOBAL_TIMEOUT = 30000

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

    res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    if res.status_code != 201:
        menu = requests.get(f"{API_URL}/{SLUG}/menu").json()
        order_payload['items'][0]['product_id'] = menu['categories'][0]['products'][0]['id']
        res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    
    order = res.json()
    order_id = order["id"]

    auth = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
    headers = {"Authorization": f"Bearer {auth['access_token']}"}

    # Garante que o pedido está pronto e pago para visibilidade no cliente
    requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    
    print(f"   ✅ Pedido {order_id[:8]} pronto e PAGO.")
    return order_id, order_payload['customer_name']

async def run_simulation():
    order_id, customer_name = await setup_order()
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=500)
        
        # --- CONTEXTO DO MOTORISTA ---
        print("\n📱 [2/5] Abrindo Painel do Entregador...")
        driver_context = await browser.new_context(viewport={"width": 400, "height": 800})
        
        # 🛡️ ANTI-INTERCEPTION: Injeta flag para desativar o Onboarding Tour
        await driver_context.add_init_script("""
            window.localStorage.setItem('mesaflow_tour_completed', 'true');
        """)
        
        driver_page = await driver_context.new_page()
        
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill('input[name="email"]', ADMIN_EMAIL)
        await driver_page.fill('input[name="password"]', ADMIN_PASS)
        await driver_page.click('button[type="submit"]')
        await driver_page.wait_for_url("**/dashboard", timeout=GLOBAL_TIMEOUT)
        
        # Navega para o painel do motorista
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # --- CONTEXTO DO CLIENTE ---
        print("👤 [3/5] Abrindo Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 400, "height": 800})
        customer_page = await customer_context.new_page()
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        
        print("   ⏳ Aguardando renderização do status...")
        try:
            await expect(customer_page.get_by_text("Pronto")).to_be_visible(timeout=20000)
            print("   ✅ Cliente visualiza: 'Pedido Pronto'.")
        except Exception as e:
            print(f"   ❌ Erro na validação visual: {e}")
            await customer_page.screenshot(path=SCREENSHOT_DIR / "failure_state.png")
            await browser.close()
            sys.exit(1)

        # --- AÇÃO: MOTORISTA PEGA O PEDIDO ---
        print("\n👉 [4/5] Motorista clicando em 'Pegar Pedido'...")
        # Localizador robusto para o botão dentro do card do cliente
        pickup_btn = driver_page.locator(f"div:has-text('{customer_name}')").get_by_role("button", name="Pegar").first
        
        # O clique agora deve funcionar pois o overlay do Joyride foi desativado via init_script
        await pickup_btn.click()

        # --- VALIDAÇÃO REAL-TIME NO CLIENTE ---
        print("⏳ [5/5] Validando atualização automática no Cliente via WebSocket...")
        try:
            await expect(customer_page.get_by_text("Em Rota")).to_be_visible(timeout=15000)
            await customer_page.screenshot(path=SCREENSHOT_DIR / "customer_en_route.png")
            print("   ✨ SUCESSO: Cliente recebeu atualização 'Em Rota' em tempo real!")
        except Exception as e:
            print(f"   ❌ Falha na atualização em tempo real: {e}")
            await browser.close()
            sys.exit(1)

        print("\n🏁 Simulação concluída com sucesso.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_simulation())
