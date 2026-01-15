# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:20:00
import asyncio
import requests
import json
import sys
import uuid
from datetime import datetime
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🎭 MESAFLOW: DUAL-SCREEN LOGISTICS ORCHESTRATOR (L6.9)
# ==============================================================================
# Simulação completa: Cliente (Pompéu/MG) <-> Entregador (Rua Padre João Porto)
# ==============================================================================

# Configurações de Rede
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

# Credenciais Admin
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

# Coordenadas Reais (Pompéu - MG)
DRIVER_START = {"lat": -19.22815, "lng": -44.94195} # Rua Padre João Porto, 1000
CUSTOMER_DEST = {"lat": -19.22448, "lng": -44.93548} # Rua João Machado, 376

def log_phase(phase, message):
    print(f"\n[{phase}/6] 🚀 {message}")

async def run_simulation():
    log_phase(0, "Iniciando Rito de Simulação Gold Master...")
    
    async with async_playwright() as p:
        # 1. SETUP: Autenticação e Criação do Pedido
        log_phase(1, "Fase de Ingestão: Criando pedido via API...")
        
        # Obter Token Admin
        auth_res = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
        token = auth_res['access_token']
        headers = {"Authorization": f"Bearer {token}"}

        # Criar Pedido de Delivery
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
            # Fallback: busca primeiro produto do menu se ID 1 falhar
            menu = requests.get(f"{API_URL}/{SLUG}/menu").json()
            order_payload['items'][0]['product_id'] = menu['categories'][0]['products'][0]['id']
            res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
        
        order = res.json()
        order_id = order["id"]
        print(f"   ✅ Pedido #{order_id[:6]} criado com sucesso.")

        # 2. LANÇAR NAVEGADORES
        log_phase(2, "Fase de Interface: Abrindo janelas simultâneas...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        
        # Contexto A: Cliente
        client_context = await browser.new_context(viewport={"width": 500, "height": 900})
        client_page = await client_context.new_page()
        await client_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
        
        # Contexto B: Entregador
        driver_context = await browser.new_context(viewport={"width": 500, "height": 900})
        # Bypass tour para não travar automação
        await driver_context.add_init_script("window.localStorage.setItem('mesaflow_tour_completed', 'true');")
        driver_page = await driver_context.new_page()
        
        # Login Driver
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill("input[name='email']", ADMIN_EMAIL)
        await driver_page.fill("input[name='password']", ADMIN_PASS)
        await driver_page.click("button[type='submit']")
        await driver_page.wait_for_url("**/dashboard")
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # 3. COZINHA: Preparo
        log_phase(3, "Fase de Produção: Simulando preparo na cozinha...")
        await client_page.bring_to_front()
        
        # Simula transições no backend
        requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
        requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
        await asyncio.sleep(3)
        
        requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
        print("   ✅ Pedido PRONTO. Notificação enviada ao entregador.")
        await asyncio.sleep(2)

        # 4. COLETA: Entregador assume o pedido
        log_phase(4, "Fase de Coleta: Entregador retirando o pedido...")
        await driver_page.bring_to_front()
        
        # Localiza o card e clica em PEGAR
        pickup_btn = driver_page.locator(f"[data-order-id='{order_id}']").get_by_test_id("driver.delivery.order.pickup")
        await pickup_btn.click()
        
        # Valida transição para modo mapa no driver
        await expect(driver_page.get_by_test_id("driver.delivery.active")).to_be_visible()
        print("   ✅ Pedido coletado. Iniciando rastreamento GPS.")

        # 5. ROTA: Simulação GPS Progressiva
        log_phase(5, "Fase de Trânsito: Simulando deslocamento em Pompéu/MG...")
        
        # Interpolação linear simples (10 passos)
        steps = 10
        for i in range(steps + 1):
            curr_lat = DRIVER_START["lat"] + (CUSTOMER_DEST["lat"] - DRIVER_START["lat"]) * (i / steps)
            curr_lng = DRIVER_START["lng"] + (CUSTOMER_DEST["lng"] - DRIVER_START["lng"]) * (i / steps)
            
            # Injeta localização via API (Simula o sensor do celular do driver)
            requests.post(
                f"{API_URL}/admin/delivery/orders/{order_id}/location",
                headers=headers,
                json={"lat": curr_lat, "lng": curr_lng}
            )
            
            percent = (i / steps) * 100
            sys.stdout.write(f"\r   Progresso da Rota: {percent:.0f}% | Lat: {curr_lat:.5f} Lng: {curr_lng:.5f}")
            sys.stdout.flush()
            
            # Alterna foco visual para o cliente ver o mapa se movendo
            if i == 2: await client_page.bring_to_front()
            if i == 8: await driver_page.bring_to_front()
            
            await asyncio.sleep(1.5)

        # 6. CONCLUSÃO: Entrega finalizada
        log_phase(6, "Fase Final: Concluindo entrega no destino...")
        await driver_page.bring_to_front()
        
        # Clica em Finalizar
        await driver_page.get_by_role("button", name="Finalizar Entrega").click()
        # Aceita o confirm() nativo
        driver_page.on("dialog", lambda dialog: dialog.accept())
        
        print("\n\n🏆 SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"   - Pedido: {order_id}")
        print(f"   - Destino: Rua João Machado, 376")
        print(f"   - Status Final: DELIVERED")
        
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\n🛑 Simulação interrompida pelo usuário.")
    except Exception as e:
        print(f"\n💥 Erro Crítico na Simulação: {e}")
        sys.exit(1)
