# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 08:58:00
import asyncio
import requests
import json
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🛵 REAL-TIME DELIVERY SIMULATION (L6.4 - VISUAL EDITION)
# ==============================================================================
# Objetivo: Simular a sincronia entre o Entregador e o Cliente Final.
# Modo: VISUAL (Headless=False) com janelas lado a lado.
# ==============================================================================

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
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

    # Garante que o pedido está pronto e pago
    requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    
    print(f"   ✅ Pedido {order_id[:8]} pronto e PAGO.")
    return order_id, order_payload['customer_name']

async def run_simulation():
    order_id, customer_name = await setup_order()

    async with async_playwright() as p:
        # 🎬 MODO VISUAL ATIVADO
        # slow_mo=1000 (1 segundo entre ações) para acompanhamento humano
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        
        # --- JANELA 1: ENTREGADOR (Lado Esquerdo) ---
        print("\n📱 [2/5] Abrindo Painel do Entregador...")
        driver_context = await browser.new_context(
            viewport={"width": 500, "height": 900},
            screen={"width": 1920, "height": 1080}
        )
        
        # Bypass Onboarding
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        
        driver_page = await driver_context.new_page()
        # Posiciona a janela à esquerda (via script de browser se suportado ou apenas viewport)
        
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill('input[name="email"]', ADMIN_EMAIL)
        await driver_page.fill('input[name="password"]', ADMIN_PASS)
        await driver_page.click('button[type="submit"]')
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # --- JANELA 2: CLIENTE (Lado Direito) ---
        print("👤 [3/5] Abrindo Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 500, "height": 900})
        customer_page = await customer_context.new_page()
        
        # Acessa a URL de acompanhamento
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        
        print("   ⏳ Aguardando renderização do status...")
        await expect(customer_page.get_by_text("Pronto")).to_be_visible(timeout=20000)
        print("   ✅ Cliente visualiza: 'Pedido Pronto'.")

        # --- AÇÃO: MOTORISTA PEGA O PEDIDO ---
        print("\n👉 [4/5] Motorista clicando em 'Pegar Pedido'...")
        # Traz a página do motorista para frente para você ver o clique
        await driver_page.bring_to_front()
        pickup_btn = driver_page.locator(f"div:has-text('{customer_name}')").get_by_role("button", name="Pegar").first
        
        # Highlight visual antes de clicar
        await pickup_btn.evaluate("el => el.style.border = '4px solid #ea580c'")
        await asyncio.sleep(1)
        await pickup_btn.click()

        # --- VALIDAÇÃO REAL-TIME NO CLIENTE ---
        print("⏳ [5/5] Validando atualização automática no Cliente via WebSocket...")
        # Traz a página do cliente para frente para você ver a mudança mágica
        await customer_page.bring_to_front()
        
        try:
            # O texto deve mudar de "Pronto" para "Em Rota" sem refresh de página
            await expect(customer_page.get_by_text("Em Rota")).to_be_visible(timeout=15000)
            print("   ✨ SUCESSO: Cliente recebeu atualização 'Em Rota' em tempo real!")
        except Exception as e:
            print(f"   ❌ Falha na atualização em tempo real: {e}")
            await asyncio.sleep(5)
            await browser.close()
            sys.exit(1)

        print("\n🏁 Simulação concluída com sucesso. Fechando em 5 segundos...")
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_simulation())
