import os
import time
import sys
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# ==============================================================================
# CONFIGURAÇÕES GERAIS
# ==============================================================================
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"
OUTPUT_DIR = "screenshots"

# Resoluções de Dispositivos
VIEWPORTS = {
    "DESKTOP": {"width": 1920, "height": 1080},
    "TABLET":  {"width": 1024, "height": 768},  # KDS / Kiosk
    "MOBILE":  {"width": 390, "height": 844}    # iPhone 12/13/14 (Garçom/Driver)
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def scroll_page(page):
    """Rola a página suavemente para ativar animações de scroll."""
    print("   ...Rolando página para ativar animações...")
    for _ in range(5):
        page.mouse.wheel(0, 500)
        time.sleep(0.5)
    # Volta ao topo rápido ou mantém onde parou? 
    # Para screenshots full_page, o playwright já captura tudo, 
    # mas o scroll garante que o lazy load carregou.
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)

def capture(page, name, folder="."):
    """Tira screenshot full page e salva na pasta organizada."""
    target_dir = os.path.join(OUTPUT_DIR, folder)
    ensure_dir(target_dir)
    
    filename = f"{target_dir}/{name}.png"
    print(f"📸 Capturando: {folder}/{name}...")
    
    try:
        # Tenta esperar a rede ficar quieta
        page.wait_for_load_state("networkidle", timeout=3000)
    except:
        pass
    
    time.sleep(1) # Estabilização visual
    page.screenshot(path=filename, full_page=True)

def run_capture_session():
    if os.path.exists(OUTPUT_DIR):
        import shutil
        shutil.rmtree(OUTPUT_DIR)
    ensure_dir(OUTPUT_DIR)

    print(f"🚀 Iniciando Auditoria Visual Completa em {BASE_URL}")

    with sync_playwright() as p:
        # Browser Launch
        browser = p.chromium.launch(headless=True)
        
        # ======================================================================
        # FASE 1: PÚBLICO & LANDING PAGE (DESKTOP)
        # ======================================================================
        print("\n--- FASE 1: Landing Page & Auth ---")
        context = browser.new_context(viewport=VIEWPORTS["DESKTOP"])
        page = context.new_page()

        # 1.1 Landing Page (Com Scroll para animações)
        try:
            page.goto(BASE_URL, timeout=10000)
            scroll_page(page) # Ativa ScrollReveal
            capture(page, "01_Home_Full", "01_Public")
        except Exception as e:
            print(f"❌ Erro ao acessar Home: {e}")
            print("   Verifique se o servidor está rodando (python run.py)")
            sys.exit(1)

        # 1.2 Telas de Auth
        page.goto(f"{BASE_URL}/admin/login")
        capture(page, "02_Login", "01_Public")

        page.goto(f"{BASE_URL}/admin/register")
        capture(page, "03_Register", "01_Public")
        
        page.goto(f"{BASE_URL}/admin/forgot-password")
        capture(page, "04_Forgot_Password", "01_Public")

        # ======================================================================
        # FASE 2: ADMIN DASHBOARD (DESKTOP)
        # ======================================================================
        print("\n--- FASE 2: Admin Dashboard ---")
        
        # Login
        page.goto(f"{BASE_URL}/admin/login")
        page.fill('input[name="email"]', ADMIN_EMAIL)
        page.fill('input[name="password"]', ADMIN_PASS)
        page.click('button[type="submit"]')
        try:
            page.wait_for_url(f"**/admin/{SLUG}/dashboard", timeout=10000)
        except:
            print("❌ Falha no login. Verifique as credenciais.")
            return
        
        # Desativar Tour
        page.evaluate("localStorage.setItem('mesaflow_tour_completed', 'true')")
        page.reload()

        # Rotas Principais
        admin_routes = [
            ("01_Dashboard", f"/admin/{SLUG}/dashboard"),
            ("02_Franquia", "/admin/franchise"),
            ("03_Cardapio", f"/admin/{SLUG}/menu"),
            ("04_Estoque", f"/admin/{SLUG}/inventory"),
            ("05_Mesas", f"/admin/{SLUG}/tables"),
            ("06_Marketing", f"/admin/{SLUG}/marketing"),
            ("07_Equipe", f"/admin/{SLUG}/team"),
            ("08_Historico", f"/admin/{SLUG}/history"),
        ]

        for name, route in admin_routes:
            page.goto(f"{BASE_URL}{route}")
            capture(page, name, "02_Admin")

        # Sub-abas de Configuração
        print("   > Navegando em Configurações...")
        page.goto(f"{BASE_URL}/admin/{SLUG}/settings")
        capture(page, "09_Config_Geral", "02_Admin")

        tabs = [
            ("Marketing", "10_Config_Marketing"),
            ("Financeiro", "11_Config_Financeiro"),
            ("Plano", "12_Config_Billing")
        ]
        
        for label, fname in tabs:
            try:
                # Tenta clicar no botão que contém o texto
                page.click(f'button:has-text("{label}")', timeout=2000)
                time.sleep(0.5)
                capture(page, fname, "02_Admin")
            except:
                print(f"⚠️ Falha ao clicar na aba {label}")

        context.close()

        # ======================================================================
        # FASE 3: APPS OPERACIONAIS (TABLET / KDS)
        # ======================================================================
        print("\n--- FASE 3: Operação (Tablet/KDS) ---")
        context_tablet = browser.new_context(viewport=VIEWPORTS["TABLET"])
        page_tablet = context_tablet.new_page()
        
        # Re-login (Novo contexto limpo)
        page_tablet.goto(f"{BASE_URL}/admin/login")
        page_tablet.fill('input[name="email"]', ADMIN_EMAIL)
        page_tablet.fill('input[name="password"]', ADMIN_PASS)
        page_tablet.click('button[type="submit"]')
        page_tablet.wait_for_url(f"**/dashboard")
        page_tablet.evaluate("localStorage.setItem('mesaflow_tour_completed', 'true')")

        # KDS
        page_tablet.goto(f"{BASE_URL}/admin/{SLUG}/kitchen")
        capture(page_tablet, "01_KDS_Kitchen", "03_Operations")

        # Kiosk (Totem)
        page_tablet.goto(f"{BASE_URL}/{SLUG}/kiosk")
        capture(page_tablet, "02_Kiosk_Attract", "03_Operations")
        
        context_tablet.close()

        # ======================================================================
        # FASE 4: APPS MÓVEIS (MOBILE)
        # ======================================================================
        print("\n--- FASE 4: Apps Móveis (Garçom/Driver/Cliente) ---")
        context_mobile = browser.new_context(
            viewport=VIEWPORTS["MOBILE"],
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )
        page_mobile = context_mobile.new_page()

        # Re-login Mobile
        page_mobile.goto(f"{BASE_URL}/admin/login")
        page_mobile.fill('input[name="email"]', ADMIN_EMAIL)
        page_mobile.fill('input[name="password"]', ADMIN_PASS)
        page_mobile.click('button[type="submit"]')
        page_mobile.wait_for_url(f"**/dashboard")
        page_mobile.evaluate("localStorage.setItem('mesaflow_tour_completed', 'true')")

        # App do Garçom
        page_mobile.goto(f"{BASE_URL}/admin/{SLUG}/waiter")
        capture(page_mobile, "01_Waiter_Tables", "04_Mobile_Apps")
        
        page_mobile.goto(f"{BASE_URL}/admin/{SLUG}/waiter/orders")
        capture(page_mobile, "02_Waiter_Orders", "04_Mobile_Apps")

        page_mobile.goto(f"{BASE_URL}/admin/{SLUG}/waiter/pos/quick?mode=takeout")
        capture(page_mobile, "03_Waiter_POS_Balcao", "04_Mobile_Apps")

        # App do Entregador
        page_mobile.goto(f"{BASE_URL}/admin/{SLUG}/driver")
        capture(page_mobile, "04_Driver_App", "04_Mobile_Apps")

        # Cardápio do Cliente (Público)
        # Logout para ver como cliente anônimo
        page_mobile.goto(f"{BASE_URL}/admin/login") # Apenas para limpar estado se necessário, mas o menu é público
        
        page_mobile.goto(f"{BASE_URL}/{SLUG}/menu")
        capture(page_mobile, "05_Customer_Menu", "04_Mobile_Apps")

        # Simular clique em produto para ver modal
        try:
            # Tenta clicar no primeiro produto disponível
            # Seletor genérico para pegar qualquer card de produto
            page_mobile.locator("text=R$").first.click()
            time.sleep(1)
            capture(page_mobile, "06_Customer_Product_Modal", "04_Mobile_Apps")
        except:
            print("⚠️ Não foi possível abrir modal de produto")

        context_mobile.close()
        browser.close()

    print(f"\n✨ Auditoria Visual Concluída! Verifique a pasta '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    run_capture_session()