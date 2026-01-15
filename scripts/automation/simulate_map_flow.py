# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 16:50:00
import asyncio
import requests
import json
import sys
import uuid
from playwright.async_api import async_playwright, expect

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def setup_delivery_order():
    unique_id = str(uuid.uuid4())[:4].upper()
    customer_name = f"MAP_HARDENED_{unique_id}"
    print(f"📦 [1/4] Gerando pedido robusto: {customer_name}")
    
    order_payload = {
        "order_type": "delivery",
        "customer_name": customer_name,
        "customer_phone": "11988887777",
        "delivery_address": "Rua Padre João Porto, 1000, Pompéu, MG",
        "payment_method": "online",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    order_id = res.json()["id"]

    auth = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
    token = auth['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    return order_id, customer_name, token

async def run_visual_simulation():
    order_id, customer_name, token = await setup_delivery_order()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        
        # --- PAINEL DO ENTREGADOR ---
        print("📱 [2/4] Abrindo Painel do Entregador...")
        driver_context = await browser.new_context(viewport={"width": 600, "height": 900})
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        driver_page = await driver_context.new_page()
        
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill('input[name="email"]', ADMIN_EMAIL)
        await driver_page.fill('input[name="password"]', ADMIN_PASS)
        await driver_page.click('button[type="submit"]')
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # --- TELA DO CLIENTE ---
        print("👤 [3/4] Abrindo Tela de Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 600, "height": 900})
        customer_page = await customer_context.new_page()
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")

        # --- AÇÃO ROBUSTA ---
        print(f"👉 [4/4] Localizando e clicando em 'PEGAR'...")
        await driver_page.bring_to_front()
        
        # Hardening: Força um reload se o card não aparecer em 5s (contorna a falta de Redis)
        try:
            await expect(driver_page.locator(f"[data-order-id='{order_id}']")).to_be_visible(timeout=5000)
        except:
            print("   ⚠️  Pedido não detectado via WS (Redis Offline?). Forçando reload...")
            await driver_page.reload()
            await expect(driver_page.locator(f"[data-order-id='{order_id}']")).to_be_visible(timeout=10000)

        # Clica no botão usando o seletor escopado por ID de pedido
        order_card = driver_page.locator(f"[data-testid='driver.delivery.order.card'][data-order-id='{order_id}']")
        await order_card.get_by_test_id("driver.delivery.order.pickup").click()

        # --- VALIDAÇÃO REAL-TIME ---
        print("⏳ Validando abertura do mapa...")
        await expect(customer_page.get_by_test_id("customer.order.step.delivering")).to_be_visible(timeout=15000)
        
        # Simula percurso GPS
        coords = [(-19.22448, -44.93548), (-19.22600, -44.93800), (-19.22815, -44.94195)]
        headers = {"Authorization": f"Bearer {token}"}
        
        for lat, lng in coords:
            requests.post(f"{API_URL}/admin/delivery/orders/{order_id}/location", headers=headers, json={"lat": lat, "lng": lng})
            print(f"📍 GPS Post: {lat}, {lng}")
            await asyncio.sleep(2)

        print("\n🏆 SUCESSO: Simulação concluída com sincronia forçada.")
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_visual_simulation())

