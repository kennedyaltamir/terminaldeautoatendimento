# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 08:35:00
import asyncio
import requests
import json
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, expect

# ==============================================================================
# 🛵 REAL-TIME DELIVERY & TRACKING SIMULATION (L6.1 - Hardened)
# ==============================================================================
# Objetivo: Simular a sincronia entre o Entregador e o Cliente Final.
# Fix v6.1: Aumento de timeouts e diagnóstico de falha de renderização.
# ==============================================================================

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
SCREENSHOT_DIR = Path("testesvisuais/realtime_delivery")
GLOBAL_TIMEOUT = 30000 # 30 segundos para operações lentas

# Credenciais
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def setup_order():
    print("🛠️  [1/5] Criando pedido de delivery via API...")
    order_payload = {
        "order_type": "delivery",
        "customer_name": f"Cliente Realtime {datetime.now().strftime('%H%M')}",
        "customer_phone": "11988887777",
        "delivery_address": "Av. Paulista, 1000, São Paulo",
        "payment_method": "online",
        "items": [{"product_id": 1, "quantity": 1}]
    }

    # Tenta criar o pedido
    res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    if res.status_code != 201:
        print("   ⚠️  Produto ID 1 não encontrado, buscando produto dinâmico...")
        menu = requests.get(f"{API_URL}/{SLUG}/menu").json()
        order_payload['items'][0]['product_id'] = menu['categories'][0]['products'][0]['id']
        res = requests.post(f"{API_URL}/{SLUG}/orders", json=order_payload)
    
    if res.status_code != 201:
        raise Exception(f"Falha ao criar pedido: {res.text}")

    order = res.json()
    order_id = order["id"]

    # Login para avançar status
    auth = requests.post(f"{API_URL}/auth/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}).json()
    headers = {"Authorization": f"Bearer {auth['access_token']}"}

    # Move para READY (Pronto para Retirada)
    requests.patch(f"{API_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})
    print(f"   ✅ Pedido {order_id[:8]} criado e movido para 'ready'.")
    return order_id, order_payload['customer_name']

async def run_simulation():
    order_id, customer_name = await setup_order()
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        # Headless=False para debug visual se necessário
        browser = await p.chromium.launch(headless=True, slow_mo=500)
        
        # --- CONTEXTO DO MOTORISTA ---
        print("\n📱 [2/5] Abrindo Painel do Entregador...")
        driver_context = await browser.new_context(
            viewport={"width": 400, "height": 800},
            permissions=["geolocation"],
            geolocation={"latitude": -23.5505, "longitude": -46.6333}
        )
        driver_page = await driver_context.new_page()
        
        # Login Driver
        await driver_page.goto(f"{BASE_URL}/admin/login")
        await driver_page.fill('input[name="email"]', ADMIN_EMAIL)
        await driver_page.fill('input[name="password"]', ADMIN_PASS)
        await driver_page.click('button[type="submit"]')
        await driver_page.wait_for_url("**/dashboard", timeout=GLOBAL_TIMEOUT)
        await driver_page.goto(f"{BASE_URL}/admin/{SLUG}/driver")

        # --- CONTEXTO DO CLIENTE ---
        print("👤 [3/5] Abrindo Acompanhamento do Cliente...")
        customer_context = await browser.new_context(viewport={"width": 400, "height": 800})
        customer_page = await customer_context.new_page()
        
        # Acessa a URL de acompanhamento do pedido
        tracking_url = f"{BASE_URL}/{SLUG}/menu?order={order_id}"
        await customer_page.goto(tracking_url)
        
        # Aguarda o carregamento da API de pedidos no frontend
        print("   ⏳ Aguardando renderização do status...")
        try:
            # Procura o texto "Pronto" no stepper ou no resumo
            # Aumentamos o timeout para 15s para compensar o dev server
            await expect(customer_page.get_by_text("Pronto", exact=False)).to_be_visible(timeout=15000)
            print("   ✅ Cliente visualiza: 'Pedido Pronto'.")
        except Exception as e:
            print(f"   ❌ Erro na validação visual: {e}")
            # Dump de diagnóstico
            html = await customer_page.content()
            (SCREENSHOT_DIR / "failure_dump.html").write_text(html, encoding="utf-8")
            await customer_page.screenshot(path=SCREENSHOT_DIR / "failure_state.png")
            print(f"   📸 Screenshot e HTML salvos em {SCREENSHOT_DIR}")
            await browser.close()
            sys.exit(1)

        # --- AÇÃO: MOTORISTA PEGA O PEDIDO ---
        print("\n👉 [4/5] Motorista clicando em 'Pegar Pedido'...")
        # Localiza o botão de pickup para este cliente específico
        pickup_btn = driver_page.locator(f"div:has-text('{customer_name}')").get_by_role("button", name="Pegar").first
        await pickup_btn.click()

        # --- VALIDAÇÃO REAL-TIME NO CLIENTE ---
        print("⏳ [5/5] Validando atualização automática no Cliente via WebSocket...")
        # O cliente deve mudar para "Em Rota" automaticamente
        try:
            await expect(customer_page.get_by_text("Em Rota")).to_be_visible(timeout=15000)
            await customer_page.screenshot(path=SCREENSHOT_DIR / "customer_en_route.png")
            print("   ✨ SUCESSO: Cliente recebeu atualização 'Em Rota' em tempo real!")
        except Exception as e:
            print(f"   ❌ Falha na atualização em tempo real: {e}")
            await browser.close()
            sys.exit(1)

        print("\n🏁 Simulação concluída com sucesso.")
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\n🛑 Simulação interrompida pelo usuário.")
    except Exception as e:
        print(f"\n💥 Erro fatal na simulação: {e}")
        sys.exit(1)
