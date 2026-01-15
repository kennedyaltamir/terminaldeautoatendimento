# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 11:00:00
import asyncio
import requests
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🛵 REAL-TIME DELIVERY & GPS SIMULATION (L6.14 - CINEMATIC EDITION)
# ==============================================================================
# Objetivo: Simular Driver aceitando pedido + Rota GPS fluida + Cliente avaliando.
# Modo: VISUAL PERSISTENTE.
# ==============================================================================

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

# Credenciais
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def setup_order():
    unique_id = str(uuid.uuid4())[:4].upper()
    customer_name = f"CLIENTE_ROTA_{unique_id}"
    
    print(f"🛠️  [1/5] Criando pedido para: {customer_name}")
    order_payload = {
        "order_type": "delivery",
        "customer_name": customer_name,
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
    token = auth['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    
    print(f"   ✅ Pedido {order_id[:8]} pronto e PAGO.")
    return order_id, customer_name, token

async def run_simulation():
    order_id, customer_name, admin_token = await setup_order()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        
        # --- JANELA 1: ENTREGADOR ---
        print("\n📱 [2/5] Abrindo Painel do Entregador...")
        driver_context = await browser.new_context(viewport={"width": 500, "height": 900})
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        driver_page = await driver_context.new_page()
        
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill('input[name="email"]', ADMIN_EMAIL)
        await driver_page.fill('input[name="password"]', ADMIN_PASS)
        await driver_page.click('button[type="submit"]')
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # --- JANELA 2: CLIENTE ---
        print("👤 [3/5] Abrindo Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 500, "height": 900})
        customer_page = await customer_context.new_page()
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        await expect(customer_page.get_by_text("Pronto")).to_be_visible(timeout=20000)

        # --- AÇÃO: CLIENTE AVALIA ---
        print("⭐ [4/5] Cliente realizando avaliação...")
        await customer_page.get_by_test_id("btn-avaliar").click()
        await customer_page.locator("button").nth(4).click() 
        await customer_page.fill("textarea", "Simulação L6.14: Rota dinâmica e GPS ativo!")
        await customer_page.get_by_text("Enviar Avaliação").click()
        print("   ✅ Avaliação enviada.")

        # --- AÇÃO: MOTORISTA PEGA O PEDIDO ---
        print("\n👉 [5/5] Motorista clicando em 'Pegar Pedido'...")
        await driver_page.bring_to_front()
        pickup_btn = driver_page.locator(f"div:has-text('{customer_name}')").get_by_role("button", name="Pegar").first
        await pickup_btn.click()

        # --- VALIDAÇÃO REAL-TIME + ROTA GPS ---
        print("⏳ Validando ROTA DINÂMICA no Cliente...")
        await customer_page.bring_to_front()
        await expect(customer_page.get_by_text("Em Rota")).to_be_visible(timeout=15000)
        
        # Simula movimento GPS fluido (15 pontos)
        print("📍 Iniciando percurso simulado (Av. Paulista)...")
        start_lat, start_lng = -23.5614, -46.6559 # MASP
        end_lat, end_lng = -23.5667, -46.6512   # Gazeta
        
        steps = 15
        for i in range(steps + 1):
            curr_lat = start_lat + (end_lat - start_lat) * (i / steps)
            curr_lng = start_lng + (end_lng - start_lng) * (i / steps)
            
            requests.post(
                f"{API_URL}/admin/delivery/orders/{order_id}/location",
                headers={"Authorization": f"Bearer {admin_token}"},
                json={"lat": curr_lat, "lng": curr_lng}
            )
            sys.stdout.write(f"\r   -> GPS Progress: {((i/steps)*100):.0f}%")
            sys.stdout.flush()
            await asyncio.sleep(1.5)

        print("\n\n🏆 SUCESSO: Rota dinâmica concluída e validada visualmente!")
        while True: await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\n🛑 Simulação encerrada.")
