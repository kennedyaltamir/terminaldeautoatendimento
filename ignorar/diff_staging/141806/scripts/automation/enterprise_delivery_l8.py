# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 15:00:00
import asyncio
import json
import sys
import os
import requests
from datetime import datetime
from playwright.async_api import async_playwright, expect
from lib.simulation_engine import SimState, StateMachine, ContractValidator, SimulationTransaction, MetricsCollector

# Configurações de Governança
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
ADMIN_CREDENTIALS = {"username": "admin@mesaflow.com", "password": "123456"}
BUILD_ID = f"GM-{datetime.now().strftime('%Y%m%d.%H%M')}"

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
            # 2. ORDER CREATION (Contract Validated)
            print("📦 [1/4] Criando Pedido (Contract Validation)...")
            t0 = time.time()
            res = requests.post(f"{API_URL}/{SLUG}/orders", json={
                "order_type": "delivery",
                "customer_name": f"L8_AUDIT_{BUILD_ID}",
                "delivery_address": "Rua João Machado, 376, Pompéu, MG",
                "items": [{"product_id": 1, "quantity": 1}]
            })
            order_data = res.json()
            ContractValidator.validate_order(order_data)
            order_id = order_data["id"]
            tx.set_order(order_id)
            
            fsm.transition_to(SimState.CREATED)
            metrics.record_transition(SimState.IDLE, SimState.CREATED, (time.time()-t0)*1000)

            # 3. BROWSER ORCHESTRATION
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            client_page = await (await browser.new_context()).new_page()
            await client_page.goto(f"{BASE_URL}/{SLUG}/menu?order={order_id}")
            
            driver_ctx = await browser.new_context()
            await driver_ctx.add_init_script("localStorage.setItem('mesaflow_tour_completed', 'true');")
            driver_page = await driver_ctx.new_page()

            # 4. DOMAIN ASSERTIONS: KITCHEN
            print("🍳 [2/4] Validando Regras de Negócio: Cozinha...")
            
            # Assert: Driver não deve ver o pedido antes de READY
            await driver_page.goto(f"{BASE_URL}/admin/login")
            await driver_page.fill("input[name='email']", ADMIN_CREDENTIALS["username"])
            await driver_page.fill("input[name='password']", ADMIN_CREDENTIALS["password"])
            await driver_page.click("button[type='submit']")
            await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")
            
            await expect(driver_page.locator(f"[data-order-id='{order_id}']")).not_to_be_visible()
            print("   ✅ Domain Assert: Pedido invisível para driver (Status: PENDING)")

            # Transição: PAID -> PREPARING
            t_start = time.time()
            requests.patch(f"{API_URL}/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
            requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "preparing"})
            fsm.transition_to(SimState.PAID)
            fsm.transition_to(SimState.PREPARING)
            
            await expect(client_page.get_by_test_id("customer.order.step.preparing")).to_be_visible()
            metrics.record_transition(SimState.CREATED, SimState.PREPARING, (time.time()-t_start)*1000)

            # Transição: READY
            t_start = time.time()
            requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
            fsm.transition_to(SimState.READY)
            await expect(client_page.get_by_text("Pedido pronto")).to_be_visible()
            metrics.record_transition(SimState.PREPARING, SimState.READY, (time.time()-t_start)*1000)

            # 5. LOGISTICS: REALISTIC GPS (Jitter & Variable Speed)
            print("🛵 [3/4] Simulando Rota Realista (GPS Jitter)...")
            await driver_page.reload() # Sincroniza lista
            await driver_page.locator(f"[data-order-id='{order_id}']").get_by_test_id("driver.delivery.order.pickup").click()
            fsm.transition_to(SimState.DISPATCHED)
            
            # Assert: Cliente vê mapa
            await expect(client_page.get_by_test_id("customer.order.map")).to_be_visible()

            # Coordenadas Pompéu
            start = (-19.22815, -44.94195)
            end = (-19.22448, -44.93548)
            
            steps = 5
            for i in range(steps + 1):
                ratio = i / steps
                lat = start[0] + (end[0] - start[0]) * ratio
                lng = start[1] + (end[1] - start[1]) * ratio
                
                requests.post(f"{API_URL}/admin/delivery/orders/{order_id}/location", 
                             headers=headers, json={"lat": lat, "lng": lng})
                
                # L8 Realism: Ruído temporal entre 1.5s e 3.5s
                await asyncio.sleep(random.uniform(1.5, 3.5))
                sys.stdout.write(f"\r   GPS Progress: {ratio*100:.0f}% | Simulating traffic...")
                sys.stdout.flush()

            # 6. FINALIZATION & GOVERNABLE EVIDENCE
            print("\n🏁 [4/4] Finalizando e Gerando Manifesto L8...")
            await driver_page.bring_to_front()
            await driver_page.get_by_role("button", name="Finalizar Entrega").click()
            driver_page.on("dialog", lambda d: d.accept())
            
            fsm.transition_to(SimState.DELIVERED)
            
            manifest = metrics.get_final_manifest("SUCCESS")
            manifest_path = f"governance/evidence/L8_MANIFEST_{order_id[:8]}.json"
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)
            
            print(f"\n🏆 BUILD {BUILD_ID} CERTIFICADA.")
            print(f"📄 Manifesto: {manifest_path}")
            
            await asyncio.sleep(2)
            await browser.close()

if __name__ == "__main__":
    import time # Garantir para Metrics
    asyncio.run(run_l8_simulation())
