# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:15:00
import asyncio
import requests
import uuid
import time
import sys
from playwright.async_api import async_playwright, expect

# Configurações
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

# Coordenadas Pompéu, MG
DRIVER_START = {"lat": -19.22815, "lng": -44.94195} # Rua Padre João Porto, 1000
CUSTOMER_DEST = {"lat": -19.22448, "lng": -44.93548} # Rua João Machado, 376

async def run_simulation():
    print("====================================================")
    print("🛵 MESAFLOW: SIMULAÇÃO CINEMÁTICA - POMPÉU/MG")
    print("====================================================")

    # 1. SETUP DO PEDIDO VIA API (Agilidade)
    print("🛠️  [1/4] Criando pedido e preparando na cozinha...")
    auth_res = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
    token = auth_res['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    # Criar pedido de delivery
    order_payload = {
        "order_type": "delivery",
        "customer_name": "Morador Pompéu",
        "customer_phone": "37999998888",
        "delivery_address": "Rua João Machado, 376, Pompéu, MG",
        "payment_method": "online",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    
    res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    if res.status_code != 201:
        # Fallback: busca primeiro produto se ID 1 falhar
        menu = requests.get(f"{API_URL}/{SLUG}/menu").json()
        order_payload['items'][0]['product_id'] = menu['categories'][0]['products'][0]['id']
        res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    
    order = res.json()
    order_id = order["id"]

    # Avançar status: Pago -> Preparando -> Pronto
    requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
    time.sleep(1)
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    print(f"   ✅ Pedido {order_id[:8]} PRONTO para entrega.")

    async with async_playwright() as p:
        # 2. ABRIR TELAS
        print("\n🌐 [2/4] Abrindo interfaces (Cliente e Entregador)...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        
        # Janela do Cliente (Esquerda)
        customer_context = await browser.new_context(viewport={"width": 500, "height": 900})
        customer_page = await customer_context.new_page()
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        
        # Janela do Entregador (Direita)
        driver_context = await browser.new_context(viewport={"width": 500, "height": 900})
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        driver_page = await driver_context.new_page()
        
        # Login Driver
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill("input[name='email']", ADMIN_EMAIL)
        await driver_page.fill("input[name='password']", ADMIN_PASS)
        await driver_page.click("button[type='submit']")
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # 3. INICIAR ENTREGA
        print("\n👉 [3/4] Entregador coletando o pedido...")
        await driver_page.bring_to_front()
        pickup_btn = driver_page.locator(f"[data-order-id='{order_id}']").get_by_test_id("driver.delivery.order.pickup")
        await pickup_btn.click()
        
        # Validar que o cliente viu a mudança
        await customer_page.bring_to_front()
        await expect(customer_page.get_by_test_id("customer.order.step.delivering")).to_be_visible(timeout=10000)
        print("   ✅ Cliente notificado: 'Em Rota'. Mapa ativado.")

        # 4. SIMULAÇÃO GPS (Trajeto Padre João Porto -> João Machado)
        print("\n📍 [4/4] Simulando deslocamento GPS em Pompéu...")
        
        # Gerar 10 pontos intermediários para suavidade
        steps = 10
        for i in range(steps + 1):
            curr_lat = DRIVER_START["lat"] + (CUSTOMER_DEST["lat"] - DRIVER_START["lat"]) * (i / steps)
            curr_lng = DRIVER_START["lng"] + (CUSTOMER_DEST["lng"] - DRIVER_START["lng"]) * (i / steps)
            
            # Injeta localização via API
            requests.post(
                f"{API_URL}/admin/delivery/orders/{order_id}/location",
                headers=headers,
                json={"lat": curr_lat, "lng": curr_lng}
            )
            
            sys.stdout.write(f"\r   Progresso: {((i/steps)*100):.0f}% | Lat: {curr_lat:.5f} Lng: {curr_lng:.5f}")
            sys.stdout.flush()
            
            # Alterna visão para o cliente ver o movimento
            if i % 3 == 0:
                await customer_page.bring_to_front()
            
            await asyncio.sleep(1.5)

        print("\n\n🏆 SIMULAÇÃO CONCLUÍDA!")
        print("O entregador chegou à Rua João Machado, 376.")
        
        # Finalização opcional
        await driver_page.bring_to_front()
        await driver_page.get_by_role("button", name="Finalizar Entrega").click()
        driver_page.on("dialog", lambda d: d.accept())
        
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\n🛑 Simulação interrompida.")

