import os
import json
from playwright.sync_api import sync_playwright

def deep_debug_print():
    print("🕵️ INICIANDO DIAGNÓSTICO PROFUNDO DE IMPRESSÃO...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. Login
        print("🔑 Logando no sistema...")
        try:
            page.goto("http://localhost:3000/admin/login")
            page.fill('input[name="email"]', "admin@mesaflow.com")
            page.fill('input[name="password"]', "123456")
            page.click('button[type="submit"]')
            page.wait_for_url("**/dashboard", timeout=15000)
        except Exception as e:
            print(f"❌ Erro no login. O servidor está rodando? {e}")
            return

        # 2. Navegar para Mesas
        print("📍 Acessando página de mesas...")
        page.goto("http://localhost:3000/admin/hamburgueria-ze/tables")
        
        # Espera carregamento da UI principal
        try:
            page.wait_for_selector("text=Gestão de Mesas", timeout=10000)
            # Espera aparecer pelo menos um card de mesa na tela normal
            page.wait_for_selector(".grid > div", timeout=5000)
        except:
            print("⚠️ Timeout: A página carregou, mas não encontrei mesas na tela principal.")

        # 3. ANÁLISE DE CONTEÚDO (Antes de simular impressão)
        print("\n--- 1. ANÁLISE DE CONTEÚDO (DOM) ---")
        
        # Verifica se o container existe
        print_layer = page.locator("#print-layer")
        if print_layer.count() == 0:
            print("❌ CRÍTICO: O elemento <div id='print-layer'> NÃO EXISTE no HTML.")
            browser.close()
            return
        
        # Conta quantos QR Codes (SVG) existem dentro do layer
        qr_count = print_layer.locator("svg").count()
        print(f"📊 QR Codes encontrados dentro do layer de impressão: {qr_count}")
        
        if qr_count == 0:
            print("❌ DIAGNÓSTICO: FALTA DE CONTEÚDO.")
            print("   O container existe, mas está vazio. O React não renderizou os QR Codes dentro dele.")
            print("   Possível causa: Estado 'tables' vazio ou erro de renderização.")
        else:
            print(f"✅ Conteúdo OK: {qr_count} mesas prontas para imprimir.")

        # 4. ANÁLISE DE ESTILO (Simulando Impressão)
        print("\n--- 2. ANÁLISE DE ESTILO (CSS PRINT) ---")
        page.emulate_media(media="print")
        
        computed = page.evaluate("""() => {
            const el = document.getElementById('print-layer');
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            return {
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity,
                width: rect.width,
                height: rect.height,
                zIndex: style.zIndex,
                backgroundColor: style.backgroundColor
            }
        }""")
        
        print(f"🎨 Propriedades Computadas no modo Print:")
        print(json.dumps(computed, indent=2))
        
        if computed['display'] == 'none':
            print("❌ ERRO: display: none detectado.")
        elif computed['height'] == 0:
            print("❌ ERRO: Altura 0 detectada. O conteúdo está colapsado.")
        elif computed['visibility'] == 'hidden':
            print("❌ ERRO: visibility: hidden detectado.")
        else:
            print("✅ Estilos parecem corretos (Visível e com dimensões).")

        # 5. EVIDÊNCIA VISUAL
        if not os.path.exists("debug_screenshots"):
            os.makedirs("debug_screenshots")
            
        # Força um fundo vermelho no body para ver se o print-layer (branco) está por cima
        page.evaluate("document.body.style.backgroundColor = 'red'")
        
        page.screenshot(path="debug_screenshots/deep_debug.png", full_page=True)
        print("\n📸 Screenshot salvo em: debug_screenshots/deep_debug.png")
        print("   (Se a imagem for toda vermelha, o layer branco não cobriu a tela)")
        print("   (Se a imagem for branca mas sem QR codes, o conteúdo está invisível)")

        browser.close()

if __name__ == "__main__":
    deep_debug_print()
