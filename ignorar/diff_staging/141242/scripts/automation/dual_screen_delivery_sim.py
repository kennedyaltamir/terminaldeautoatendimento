# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:20:00
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
    print("🎭 MESAFLOW: SIMULAÇÃO DUAL-SCREEN (CLIENTE & DRIVER)")
    print("====================================================")

    async with async_playwright() as p:
        # 1. INICIAR NAVEGADOR
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        
        # --- SETUP JANELA DO CLIENTE (ESQUERDA) ---
        customer_context = await browser.new_context(viewport={"width": 500, "height": 900})
        customer_page = await customer_context.new_page()
        
        # --- SETUP JANELA DO ENTREGADOR (DIREITA) ---
        driver_context = await browser.new_context(viewport={"width": 500, "height": 900})
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        driver_page = await driver_context.new_page()

        # 2. CRIAR PEDIDO INICIAL
        print("🛠️  [1/6] Criando pedido de delivery...")
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
            menu = requests.get(f"{API_URL}/{SLUG}/menu").json()
            order_payload['items'][0]['product_id'] = menu['categories'][0]['products'][0]['id']
            res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
        
        order = res.json()
        order_id = order["id"]
        print(f"   ✅ Pedido #{order_id[:6]} criado.")

        # 3. POSICIONAR JANELAS E CARREGAR
        print("🌐 [2/6] Carregando interfaces...")
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        
        # Login Driver
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill("input[name='email']", ADMIN_EMAIL)
        await driver_page.fill("input[name='password']", ADMIN_PASS)
        await driver_page.click("button[type='submit']")
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # 4. SIMULAR COZINHA (ESTADOS INICIAIS)
        print("\n🍳 [3/6] Cozinha: Iniciando preparo...")
        auth_res = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
        token = auth_res['access_token']
        headers = {"Authorization": f"Bearer {token}"}

        # Pago -> Preparando
        requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
        requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
        await asyncio.sleep(3)

        print("✅ [4/6] Cozinha: Pedido PRONTO!")
        requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
        
        # 5. ENTREGADOR COLETA
        print("\n🛵 [5/6] Entregador: Coletando pedido na Rua Padre João Porto...")
        await driver_page.bring_to_front()
        # Localiza o botão PEGAR específico para este pedido
        pickup_btn = driver_page.locator(f"[data-order-id='{order_id}']").get_by_test_id("driver.delivery.order.pickup")
        await pickup_btn.click()

        # 6. SIMULAÇÃO GPS REAL-TIME
        print("\n📍 [6/6] Em Rota: Simulando deslocamento GPS...")
        steps = 8
        for i in range(steps + 1):
            curr_lat = DRIVER_START["lat"] + (CUSTOMER_DEST["lat"] - DRIVER_START["lat"]) * (i / steps)
            curr_lng = DRIVER_START["lng"] + (CUSTOMER_DEST["lng"] - DRIVER_START["lng"]) * (i / steps)
            
            # Injeta localização via API
            requests.post(
                f"{API_URL}/admin/delivery/orders/{order_id}/location",
                headers=headers,
                json={"lat": curr_lat, "lng": curr_lng}
            )
            
            sys.stdout.write(f"\r   Progresso: {((i/steps)*100):.0f}% | Motorista se movendo...")
            sys.stdout.flush()
            
            # Alterna foco para o cliente ver o mapa
            if i == 2: await customer_page.bring_to_front()
            await asyncio.sleep(2)

        print("\n\n🏁 Chegada ao destino: Rua João Machado, 376.")
        await driver_page.bring_to_front()
        
        # Finalizar
        await driver_page.get_by_role("button", name="Finalizar Entrega").click()
        driver_page.on("dialog", lambda d: d.accept())
        
        print("\n🏆 SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\n🛑 Simulação interrompida.")
