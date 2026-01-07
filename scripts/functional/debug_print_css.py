import os
import time
import socket
from playwright.sync_api import sync_playwright

def is_port_open(host, port):
    """Verifica se a porta 3000 está aberta (Servidor rodando)"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def debug_print():
    print("🖨️ Iniciando Debug de Impressão...")

    if not is_port_open("localhost", 3000):
        print("\n❌ ERRO: O servidor Frontend não está rodando na porta 3000.")
        print("👉 Solução: Abra outro terminal e rode 'python run.py' antes de executar este script.\n")
        return

    with sync_playwright() as p:
        print("🌍 Abrindo navegador...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. Login
        print("🔑 Realizando login...")
        try:
            page.goto("http://localhost:3000/admin/login", timeout=10000)
            page.fill('input[name="email"]', "admin@mesaflow.com")
            page.fill('input[name="password"]', "123456")
            page.click('button[type="submit"]')
            page.wait_for_url("**/dashboard", timeout=15000)
        except Exception as e:
            print(f"❌ Falha no login: {e}")
            browser.close()
            return
        
        # 2. Ir para Mesas
        print("📍 Navegando para Gestão de Mesas...")
        page.goto("http://localhost:3000/admin/hamburgueria-ze/tables")
        
        # Espera a página carregar e o botão de imprimir aparecer
        try:
            page.wait_for_selector("text=Gestão de Mesas", timeout=10000)
        except:
            print("⚠️ Timeout esperando página de mesas. Tirando print do estado atual...")
        
        # 3. Simular Impressão
        print("📸 Capturando estado de impressão (CSS Print)...")
        
        # Força o CSS de media print
        page.emulate_media(media="print")
        
        # Tira screenshot
        if not os.path.exists("debug_screenshots"):
            os.makedirs("debug_screenshots")
            
        output_path = "debug_screenshots/print_preview.png"
        page.screenshot(path=output_path, full_page=True)
        print(f"✅ Screenshot salvo em: {output_path}")
        
        # Verifica se o elemento de impressão está visível no DOM
        # O elemento com classe 'print:block' deve estar visível quando media=print
        is_visible = page.evaluate("""() => {
            // Tenta achar o container de impressão
            const el = document.querySelector('.print\\\\:block');
            if (!el) return false;
            
            const style = window.getComputedStyle(el);
            // Verifica se não está oculto
            return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        }""")
        
        if is_visible:
            print("✅ DIAGNÓSTICO: O container de impressão está VISÍVEL para o navegador.")
            print("   Se a folha sai branca, pode ser configuração da impressora ou falta de conteúdo dentro do container.")
        else:
            print("❌ DIAGNÓSTICO: O container de impressão está OCULTO.")
            print("   Possível conflito de CSS (Tailwind). Verifique se 'hidden' está sobrescrevendo 'print:block'.")
            
        browser.close()

if __name__ == "__main__":
    debug_print()
