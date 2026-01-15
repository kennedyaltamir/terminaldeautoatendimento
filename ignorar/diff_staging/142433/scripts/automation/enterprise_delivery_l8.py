# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 15:10:00
import asyncio
import json
import sys
import os
import requests
import time
import random
from datetime import datetime
from playwright.async_api import async_playwright, expect
from lib.simulation_engine import SimState, StateMachine, ContractValidator, SimulationTransaction, MetricsCollector

# Configurações de Governança
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_CREDENTIALS = {"username": "admin@mesaflow.com", "password": "123456"}
BUILD_ID = f"GM-{datetime.now().strftime('%Y%m%d.%H%M')}"

# Coordenadas Pompéu/MG
START_COORD = (-19.22815, -44.94195)
END_COORD = (-19.22448, -44.93548)

async def run_l8_simulation():
    print(f"🧬 MESAFLOW L8 AUTONOMOUS QUALITY SYSTEM | Build: {BUILD_ID}")
    
    fsm = StateMachine()
    metrics = MetricsCollector(BUILD_ID)
    
    # 1. AUTHENTICATION (Pre-flight)
    auth_res = requests.post(f"{API_URL}/auth/token", data=ADMIN_CREDENTIALS).json()
    token = auth_res['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    with SimulationTransaction(API_URL, SLUG, token) as tx:
        async with async_playwright() as p:
            # 2. ORDER CREATION
            print("📦 [1/5] Criando Pedido Real (Persona: Cliente)...")
            t0 = time.time()
            res = requests.post(f"{API_URL}/{SLUG}/orders", json={
                "order_type": "delivery",
                "customer_name": f"L8_SIM_{BUILD_ID}",
                "customer_phone": "37999998888",
                "delivery_address": "Rua João Machado, 376, Pompéu, MG",
                "payment_method": "online",
                "items": [{"product_id": 1, "quantity": 1}]
            })
            order_data = res.json()
            ContractValidator.validate_order(order_data)
            order_id = order_data["id"]
            tx.set_order(order_id)
            
            fsm.transition_to(SimState.CREATED)
            metrics.record_transition(SimState.IDLE, SimState.CREATED, (time.time()-t0)*1000)

            # 3. BROWSER SETUP
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            client_page = await (await browser.new_context()).new_page()
            await client_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
            
            driver_ctx = await browser.new_context()
            await driver_ctx.add_init_script("localStorage.setItem('mesaflow_tour_completed', 'true');")
            driver_page = await driver_ctx.new_page()

            # 4. KITCHEN OPERATIONS
            print("🍳 [2/5] Processando na Cozinha (Persona: Operador)...")
            t_start = time.time()
            requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
            requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
            fsm.transition_to(SimState.PAID)
            fsm.transition_to(SimState.PREPARING)
            
            await expect(client_page.get_by_test_id("customer.order.step.preparing")).to_be_visible(timeout=10000)
            
            requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
            fsm.transition_to(SimState.READY)
            await expect(client_page.get_by_text("Pedido pronto")).to_be_visible(timeout=10000)
            metrics.record_transition(SimState.PREPARING, SimState.READY, (time.time()-t_start)*1000)

            # 5. LOGISTICS & TELEMETRY (FIXED FLOW)
            print("🛵 [3/5] Iniciando Entrega e Telemetria (Persona: Driver)...")
            await driver_page.goto(f"{BASE_URL}/admin/login")
            await driver_page.fill("input[name='email']", ADMIN_CREDENTIALS["username"])
            await driver_page.fill("input[name='password']", ADMIN_CREDENTIALS["password"])
            await driver_page.click("button[type='submit']")
            await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")
            
            # Coleta o pedido
            await driver_page.locator(f"[data-order-id='{order_id}']").get_by_test_id("driver.delivery.order.pickup").click()
            fsm.transition_to(SimState.DISPATCHED)

            # 🛡️ L8 FIX: Injeta o primeiro ponto GPS ANTES de verificar o mapa
            # O mapa é "lazy-loaded" baseado na existência de coordenadas
            requests.post(f"{API_URL}/admin/delivery/orders/{order_id}/location", 
                         headers=headers, json={"lat": START_COORD[0], "lng": START_COORD[1]})
            
            print("   📍 GPS Inicial injetado. Validando ativação do mapa no cliente...")
            
            # Assert com timeout estendido e mensagem de erro de domínio
            await expect(client_page.get_by_test_id("customer.order.map")).to_be_visible(
                timeout=15000,
                message="FALHA DE DOMÍNIO: Mapa não ativado após despacho e telemetria inicial."
            )

            # Simulação de Rota com Jitter
            steps = 5
            for i in range(1, steps + 1):
                ratio = i / steps
                lat = START_COORD[0] + (END_COORD[0] - START_COORD[0]) * ratio
                lng = START_COORD[1] + (END_COORD[1] - START_COORD[1]) * ratio
                
                requests.post(f"{API_URL}/admin/delivery/orders/{order_id}/location", 
                             headers=headers, json={"lat": lat, "lng": lng})
                
                await asyncio.sleep(random.uniform(1.5, 3.0))
                sys.stdout.write(f"\r   Progresso GPS: {ratio*100:.0f}% | Movendo ícone no cliente...")
                sys.stdout.flush()

            # 6. FINALIZATION
            print("\n🏁 [4/5] Finalizando Entrega no Destino...")
            await driver_page.bring_to_front()
            await driver_page.get_by_role("button", name="Finalizar Entrega").click()
            driver_page.on("dialog", lambda d: d.accept())
            
            fsm.transition_to(SimState.DELIVERED)
            await expect(client_page.get_by_text("Pedido entregue")).to_be_visible(timeout=10000)

            # 7. MANIFEST GENERATION
            print("[5/5] Gerando Manifesto de Auditoria L8...")
            manifest = metrics.get_final_manifest("SUCCESS")
            manifest_path = f"governance/evidence/L8_MANIFEST_{order_id[:8]}.json"
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)
            
            print(f"\n🏆 SIMULAÇÃO CONCLUÍDA: Build {BUILD_ID} Selada.")
            await asyncio.sleep(2)
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_l8_simulation())
