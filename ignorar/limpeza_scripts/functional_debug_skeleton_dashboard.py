import os
import time
import json
from playwright.sync_api import sync_playwright

# Configurações
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
TARGET_URL = f"{BASE_URL}/admin/{SLUG}/dashboard"
SCREENSHOT_DIR = "debug_screenshots"

def run_debug():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    print(f"🕵️ Iniciando Diagnóstico de Vigilância: Dashboard Skeletons")

    with sync_playwright() as p:
        # headless=False para observação humana se necessário
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()

        # 1. Preparar ambiente (Token e Tour Off)
        context.add_init_script("""
            localStorage.setItem('mesaflow_access_token', 'fake-debug-token');
            localStorage.setItem('mesaflow_user_role', 'owner');
            localStorage.setItem('mesaflow_tour_completed', 'true');
        """)

        page = context.new_page()

        # 2. Configurar Interceptação com Delay Controlado
        api_called = False

        def mock_metrics(route):
            nonlocal api_called
            print("📡 API Detectada! Iniciando delay de 3s para observação visual...")
            api_called = True
            time.sleep(3)
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({
                    "total_revenue": 1250.50,
                    "total_orders": 42,
                    "average_ticket": 29.77,
                    "top_products": [{"name": "X-Bacon", "count": 20, "revenue": 600}],
                    "sales_chart": [{"date": "05/01", "value": 1250}],
                    "sales_by_hour": [{"hour": 12, "total": 500, "count": 10}],
                    "product_performance": [],
                    "ticket_evolution": []
                })
            )

        page.route("**/api/admin/metrics*", mock_metrics)
        page.route("**/api/admin/company/me", lambda route: route.fulfill(status=200, body=json.dumps({"name":"Loja Teste"})))

        try:
            print(f"🚀 Navegando para {TARGET_URL}...")
            page.goto(TARGET_URL, wait_until="commit")

            # 3. Vigilância Ativa de Skeletons
            # Vamos tentar capturar o skeleton várias vezes por 2 segundos
            print("🔍 Vigilância Ativa: Tentando capturar Skeletons em tempo real...")
            
            found_skeleton = False
            for i in range(20): # Tenta 20 vezes (a cada 100ms)
                count = page.locator(".animate-pulse").count()
                if count > 0:
                    print(f"✨ MOMENTO EXATO: Skeletons detectados ({count} elementos) no ciclo {i}!")
                    page.screenshot(path=f"{SCREENSHOT_DIR}/01_skeleton_detected.png")
                    found_skeleton = True
                    break
                time.sleep(0.1)

            if not found_skeleton:
                print("❌ FALHA: Mesmo com vigilância, os skeletons não foram capturados pelo robô.")
                print("   Possível causa: A página está carregando dados cacheados instantaneamente.")
                page.screenshot(path=f"{SCREENSHOT_DIR}/01_fail_not_found.png")

            # 4. Aguardar Transição para Dados Reais
            print("⌛ Aguardando renderização final dos dados...")
            page.wait_for_selector("text=Faturamento", timeout=10000)
            
            # Verificar se sumiram
            final_count = page.locator(".animate-pulse").count()
            if final_count == 0:
                print("✅ Skeletons removidos com sucesso. Dados reais na tela.")
                page.screenshot(path=f"{SCREENSHOT_DIR}/02_final_data.png")
            else:
                print(f"⚠️  AVISO: Ainda restam {final_count} skeletons ativos.")

        except Exception as e:
            print(f"🔥 Erro crítico no script: {e}")

        finally:
            browser.close()
            print(f"\n📸 Verifique os resultados em '{SCREENSHOT_DIR}/'")

if __name__ == "__main__":
    run_debug()
