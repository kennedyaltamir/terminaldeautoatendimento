
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 14:40:00
import webbrowser
import time
import sys

# Configuração
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"

# Rotas Mapeadas para Inspeção Visual
ROUTES = {
    "1. PÚBLICAS (Landing & Trust)": [
        "/",
        "/trust",
        "/trust/status",
        "/trust/security",
        "/offline"
    ],
    "2. TENANT PÚBLICO (Cliente Final)": [
        f"/{SLUG}/menu",
        f"/{SLUG}/kiosk",
        f"/{SLUG}/monitor"
    ],
    "3. ADMINISTRAÇÃO (Requer Login)": [
        "/admin/login",
        "/admin/register",
        f"/admin/{SLUG}/dashboard",
        f"/admin/{SLUG}/kitchen",     # KDS
        f"/admin/{SLUG}/waiter",      # POS Garçom
        f"/admin/{SLUG}/delivery",    # Logística
        f"/admin/{SLUG}/expeditor",   # Expedição
        f"/admin/{SLUG}/menu",        # Gestão de Cardápio
        f"/admin/{SLUG}/tables",      # Gestão de Mesas
        f"/admin/{SLUG}/inventory",   # Estoque
        f"/admin/{SLUG}/audit",       # Auditoria
        f"/admin/{SLUG}/settings"     # Configurações
    ]
}

def open_tabs():
    print(f"🚀 Iniciando Abertura de Abas de QA para: {BASE_URL}")
    print("⚠️  DICA: Mantenha o Console do Navegador (F12) aberto para ver erros de JS/Rede.")
    print("----------------------------------------------------------------")

    total_tabs = sum(len(urls) for urls in ROUTES.values())
    print(f"Serão abertas {total_tabs} abas. Pressione CTRL+C para cancelar em 3 segundos...")
    try:
        time.sleep(3)
    except KeyboardInterrupt:
        print("\nCancelado.")
        sys.exit(0)

    for category, urls in ROUTES.items():
        print(f"\n📂 {category}")
        for path in urls:
            full_url = f"{BASE_URL}{path}"
            print(f"   -> Abrindo: {full_url}")
            try:
                webbrowser.open(full_url)
                # Delay para não travar o navegador
                time.sleep(1.5) 
            except Exception as e:
                print(f"      ❌ Erro ao abrir: {e}")

    print("\n✨ Todas as abas foram disparadas.")
    print("👉 Verifique o terminal do 'npm run dev' para erros de renderização (500).")
    print("👉 Verifique o Console (F12) para erros de hidratação ou API (400/404).")

if __name__ == "__main__":
    open_tabs()

