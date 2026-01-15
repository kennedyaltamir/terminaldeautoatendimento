# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:10:00
import asyncio
import requests
import uuid
import time
import sys
from playwright.async_api import async_playwright, expect

# Configurações de Ambiente
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def run_simulation():
    print("====================================================")
    print("🍔 MESAFLOW: SIMULAÇÃO DE PEDIDO PONTA-A-PONTA")
    print("====================================================")

    async with async_playwright() as p:
        # 1. INICIAR NAVEGADOR (Modo Visível)
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        
        # --- FLUXO DO CLIENTE ---
        customer_context = await browser.new_context(viewport={"width": 450, "height": 850})
        customer_page = await customer_context.new_page()
        
        print(f"🌐 [CLIENTE] Acessando cardápio: {SLUG}...")
        await customer_page.goto(f"{BASE_URL}/{SLUG}/menu")
        
        # Selecionar Produto (X-Bacon do Seed)
        print("🛒 [CLIENTE] Escolhendo produto...")
        product_card = customer_page.locator("div").filter(has_text="X-Bacon").first
        await product_card.click()
        
        # Adicionar ao Carrinho
        await customer_page.get_by_role("button", name="Adicionar ao Pedido").click()
        
        # Ir para o Carrinho
        await customer_page.get_by_role("button", name="Ver Pedido").click()
        
        # Preencher Dados de Entrega
        customer_name = f"Simulador_{str(uuid.uuid4())[:4]}"
        print(f"📝 [CLIENTE] Finalizando pedido para: {customer_name}")
        
        await customer_page.fill("input[placeholder*='Seu nome']", customer_name)
        await customer_page.fill("input[placeholder*='Telefone']", "11988887777")
        await customer_page.fill("textarea[placeholder*='Endereço']", "Rua Padre João Porto, 1000, Pompéu, MG")
        
        # Selecionar Delivery e Pagamento Online (Simulado)
        await customer_page.click("text=Delivery")
        await customer_page.click("text=Pagar Online")
        
        # Enviar Pedido
        await customer_page.get_by_role("button", name="Confirmar Pedido").click()
        
        # Aguardar Redirecionamento para Status
        await customer_page.wait_for_url("**/menu?order=**")
        order_url = customer_page.url
        order_id = order_url.split("order=")[1]
        print(f"✅ [SISTEMA] Pedido gerado com sucesso! ID: {order_id}")

        # --- FLUXO DO ADMIN (PREPARO) ---
        print("\n👨‍🍳 [ADMIN] Preparando pedido na cozinha...")
        # Autenticação via API para agilizar o preparo
        auth_res = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
        token = auth_res['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Simula: Aceitar -> Preparar -> Pronto
        requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
        requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
        time.sleep(2)
        requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
        print("✅ [ADMIN] Pedido pronto para retirada.")

        # --- FLUXO DO ENTREGADOR ---
        print("\n🛵 [DRIVER] Entregador assumindo a rota...")
        driver_context = await browser.new_context(viewport={"width": 450, "height": 850})
        # Bypass tour
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        driver_page = await driver_context.new_page()
        
        # Login Admin/Driver
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill("input[name='email']", ADMIN_EMAIL)
        await driver_page.fill("input[name='password']", ADMIN_PASS)
        await driver_page.click("button[type='submit']")
        await driver_page.wait_for_url("**/dashboard")
        
        # Ir para Painel Driver
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")
        
        # Localizar e Pegar Pedido
        pickup_btn = driver_page.locator(f"[data-order-id='{order_id}']").get_by_test_id("driver.delivery.order.pickup")
        await pickup_btn.click()
        print("🚀 [DRIVER] Rota iniciada! Simulando GPS...")

        # --- SIMULAÇÃO GPS REAL-TIME ---
        # Coordenadas de Pompéu, MG (Trajeto simulado)
        path = [
            (-19.22448, -44.93548), # Origem
            (-19.22550, -44.93700),
            (-19.22650, -44.93900),
            (-19.22750, -44.94050),
            (-19.22815, -44.94195)  # Destino
        ]

        for i, (lat, lng) in enumerate(path):
            # Envia localização via API (Simulando o sensor do celular)
            requests.post(
                f"{API_URL}/admin/delivery/orders/{order_id}/location",
                headers=headers,
                json={"lat": lat, "lng": lng}
            )
            print(f"📍 [GPS] Atualização {i+1}/{len(path)}: {lat}, {lng}")
            
            # Foca na página do cliente para ver o mapa se movendo
            await customer_page.bring_to_front()
            await asyncio.sleep(2)

        print("\n🏁 [DRIVER] Chegou ao destino. Finalizando entrega...")
        await driver_page.bring_to_front()
        await driver_page.get_by_role("button", name="Finalizar Entrega").click()
        # Aceita o confirm() do navegador
        driver_page.on("dialog", lambda dialog: dialog.accept())
        
        print("\n🏆 SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        print("O cliente acompanhou todo o trajeto em tempo real via WebSocket.")
        
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\n🛑 Simulação interrompida.")
