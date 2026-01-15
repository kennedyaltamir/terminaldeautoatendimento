# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 09:10:00
import asyncio
import requests
import json
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🛵 REAL-TIME DELIVERY & FEEDBACK SIMULATION (L6.5 - FULL EXPERIENCE)
# ==============================================================================
# Objetivo: Simular Driver aceitando pedido + Cliente avaliando e rastreando.
# Modo: VISUAL PERSISTENTE (Telas ficam abertas no final).
# ==============================================================================

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

# Credenciais
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def setup_order():
    print("🛠️  [1/5] Criando pedido de delivery via API...")
    order_payload = {
        "order_type": "delivery",
        "customer_name": f"Cliente VIP {datetime.now().strftime('%H%M')}",
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
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        
        # --- JANELA 1: ENTREGADOR (Lado Esquerdo) ---
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

        # --- JANELA 2: CLIENTE (Lado Direito) ---
        print("👤 [3/5] Abrindo Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 500, "height": 900})
        customer_page = await customer_context.new_page()
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        
        print("   ⏳ Aguardando renderização do status...")
        await expect(customer_page.get_by_text("Pronto")).to_be_visible(timeout=20000)

        # --- AÇÃO: CLIENTE AVALIA O ESTABELECIMENTO ---
        print("⭐ [4/5] Cliente realizando avaliação...")
        await customer_page.get_by_test_id("btn-avaliar").click()
        # Clica na 5ª estrela
        await customer_page.locator("button").nth(4).click() 
        await customer_page.fill("textarea", "Entrega super rápida e comida quente! Recomendo.")
        await customer_page.get_by_text("Enviar Avaliação").click()
        print("   ✅ Avaliação enviada com sucesso.")

        # --- AÇÃO: MOTORISTA PEGA O PEDIDO ---
        print("\n👉 [5/5] Motorista clicando em 'Pegar Pedido'...")
        await driver_page.bring_to_front()
        pickup_btn = driver_page.locator(f"div:has-text('{customer_name}')").get_by_role("button", name="Pegar").first
        await pickup_btn.evaluate("el => el.style.border = '4px solid #ea580c'")
        await pickup_btn.click()

        # --- VALIDAÇÃO REAL-TIME NO CLIENTE ---
        print("⏳ Validando atualização de ROTA no Cliente...")
        await customer_page.bring_to_front()
        
        # O texto deve mudar para "Em Rota" e mostrar o mapa
        await expect(customer_page.get_by_text("Em Rota")).to_be_visible(timeout=15000)
        await expect(customer_page.get_by_text("Motorista a caminho!")).to_be_visible()
        
        print("   ✨ SUCESSO: Cliente visualizando rota e status 'Em Rota'!")
        print("\n🏁 Simulação concluída. As janelas permanecerão abertas para inspeção.")
        
        # Mantém o script rodando para as janelas não fecharem
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\n🛑 Simulação encerrada pelo usuário.")
