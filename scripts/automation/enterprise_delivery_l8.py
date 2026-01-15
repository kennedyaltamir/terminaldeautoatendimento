# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:50:00
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
    print(f"🧬 MESAFLOW L8.8 AUTONOMOUS QUALITY SYSTEM | Build: {BUILD_ID}")
    
    fsm = StateMachine()
    metrics = MetricsCollector(BUILD_ID)
    
    # 1. AUTHENTICATION (Pre-flight)
    auth_res = requests.post(f"{API_URL}/auth/token", data=ADMIN_CREDENTIALS).json()
    token = auth_res['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    with SimulationTransaction(API_URL, SLUG, token) as tx:
        async with async_playwright() as p:
            # 2. ORDER CREATION
            print("📦 [1/5] Ingestão de Pedido (Contract Validation)...")
            t0 = time.time()
            res = requests.post(f"{API_URL}/{SLUG}/orders", json={
                "order_type": "delivery",
                "customer_name": f"L8_AUDIT_{BUILD_ID}",
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
            
            # Contexto do Cliente com permissão de GPS
            client_ctx = await browser.new_context(
                viewport={"width": 450, "height": 800},
                permissions=["geolocation"]
            )
            client_page = await client_ctx.new_page()
            await client_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
            
            # Contexto do Entregador com permissão de GPS e bypass de tour
            driver_ctx = await browser.new_context(
                viewport={"width": 450, "height": 800},
                permissions=["geolocation"]
            )
            await driver_ctx.add_init_script("localStorage.setItem('mesaflow_tour_completed', 'true');")
            driver_page = await driver_ctx.new_page()

            # 4. KITCHEN OPERATIONS
            print("🍳 [2/5] Máquina de Estados: Cozinha...")
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

            # 5. LOGISTICS & TELEMETRY
            print("🛵 [3/5] Operação Logística: Despacho e Telemetria...")
            await driver_page.goto(f"{BASE_URL}/admin/login")
            await driver_page.fill("input[name='email']", ADMIN_CREDENTIALS["username"])
            await driver_page.fill("input[name='password']", ADMIN_CREDENTIALS["password"])
            await driver_page.click("button[type='submit']")
            await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")
            
            # Coleta o pedido
            pickup_btn = driver_page.locator(f"[data-order-id='{order_id}']").get_by_test_id("driver.delivery.order.pickup")
            await pickup_btn.click()
            fsm.transition_to(SimState.DISPATCHED)

            # Injeção de Telemetria Inicial (Gatilho de Mapa)
            requests.post(f"{API_URL}/admin/delivery/orders/{order_id}/location", 
                         headers=headers, json={"lat": START_COORD[0], "lng": START_COORD[1]})
            
            await expect(client_page.get_by_test_id("customer.order.map")).to_be_visible(timeout=15000)

            # Rota com Jitter
            steps = 3 # Reduzido para agilizar validação final
            for i in range(1, steps + 1):
                ratio = i / steps
                lat = START_COORD[0] + (END_COORD[0] - START_COORD[0]) * ratio
                lng = START_COORD[1] + (END_COORD[1] - START_COORD[1]) * ratio
                
                requests.post(f"{API_URL}/admin/delivery/orders/{order_id}/location", 
                             headers=headers, json={"lat": lat, "lng": lng})
                
                await asyncio.sleep(2)
                sys.stdout.write(f"\r   GPS Progress: {ratio*100:.0f}% | Telemetria ativa...")
                sys.stdout.flush()

            # 6. FINALIZATION
            print("\n🏁 [4/5] Conclusão de Entrega e Auditoria...")
            await driver_page.bring_to_front()
            
            finish_btn = driver_page.get_by_test_id("driver.delivery.finish-btn")
            await expect(finish_btn).to_be_visible(timeout=10000)
            
            # Aceita o confirm() nativo
            driver_page.on("dialog", lambda d: d.accept())
            await finish_btn.click()
            
            fsm.transition_to(SimState.DELIVERED)
            
            # Valida a nova Success View no Cliente
            await client_page.bring_to_front()
            await expect(client_page.get_by_text("Pedido entregue")).to_be_visible(timeout=15000)
            print("   ✅ Cliente visualizou tela de sucesso final.")

            # 7. MANIFEST GENERATION
            print("[5/5] Selagem de Evidência L8.8...")
            manifest = metrics.get_final_manifest("SUCCESS")
            manifest_path = f"governance/evidence/L8_MANIFEST_{order_id[:8]}.json"
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)
            
            print(f"\n🏆 BUILD {BUILD_ID} CERTIFICADA COM SUCESSO.")
            await asyncio.sleep(2)
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_l8_simulation())

