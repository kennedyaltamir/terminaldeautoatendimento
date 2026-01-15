# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:10:00
import asyncio
import requests
import json
import sys
import uuid
from playwright.async_api import async_playwright, expect

# Configurações
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def setup_delivery_order():
    """Cria um pedido e o coloca no estado 'Pronto para Coleta'."""
    unique_id = str(uuid.uuid4())[:4].upper()
    customer_name = f"MAP_TEST_{unique_id}"
    print(f"📦 [1/4] Gerando pedido de teste: {customer_name}")
    
    # 1. Criar pedido
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

    # 2. Obter Token
    auth = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
    token = auth['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Pagar e Deixar Pronto
    requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    
    print(f"   ✅ Pedido {order_id[:8]} está pronto para ser pego.")
    return order_id, customer_name, token

async def run_visual_simulation():
    order_id, customer_name, token = await setup_delivery_order()
    
    async with async_playwright() as p:
        # Abre o navegador visível (Headless=False)
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        
        # --- LADO DO ENTREGADOR ---
        print("📱 [2/4] Abrindo Painel do Entregador...")
        driver_context = await browser.new_context(viewport={"width": 600, "height": 900})
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        driver_page = await driver_context.new_page()
        
        # Login
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill('input[name="email"]', ADMIN_EMAIL)
        await driver_page.fill('input[name="password"]', ADMIN_PASS)
        await driver_page.click('button[type="submit"]')
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # --- LADO DO CLIENTE ---
        print("👤 [3/4] Abrindo Tela de Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 600, "height": 900})
        customer_page = await customer_context.new_page()
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")

        # --- AÇÃO: CLICAR EM PEGAR ---
        print(f"👉 [4/4] Clicando em 'PEGAR' para {customer_name}...")
        await driver_page.bring_to_front()
        # Localiza o card pelo nome do cliente e clica no botão PEGAR dentro dele
        await driver_page.locator(f"div:has-text('{customer_name}')").get_by_role("button", name="PEGAR").click()

        # --- VALIDAÇÃO DO MAPA ---
        print("⏳ Validando surgimento do mapa e movimentação real-time...")
        await expect(customer_page.get_by_text("Em Rota")).to_be_visible(timeout=10000)
        
        # Simula percurso GPS enviando via API (isso fará o ícone 🛵 se mexer no mapa)
        coords = [
            (-19.22448, -44.93548),
            (-19.22550, -44.93750),
            (-19.22700, -44.93950),
            (-19.22815, -44.94195)
        ]
        
        headers = {"Authorization": f"Bearer {token}"}
        for lat, lng in coords:
            requests.post(
                f"{API_URL}/admin/delivery/orders/{order_id}/location",
                headers=headers,
                json={"lat": lat, "lng": lng}
            )
            print(f"📍 GPS Update: {lat}, {lng}")
            await asyncio.sleep(2)

        print("\n🏆 SIMULAÇÃO CONCLUÍDA: O mapa abriu e o entregador se moveu em ambas as telas!")
        # Aguarda um pouco para o usuário ver o resultado final antes de fechar
        await asyncio.sleep(10)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_visual_simulation())
