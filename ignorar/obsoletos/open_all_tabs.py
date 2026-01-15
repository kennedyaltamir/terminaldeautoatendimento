import webbrowser
import time
import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================
BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"

# Rotas categorizadas para evitar redirecionamentos em massa
AUTH_ROUTE = "/admin/login"

PUBLIC_ROUTES = [
    f"/{SLUG}/menu",                # Cardápio Digital
    f"/{SLUG}/kiosk",               # Modo Totem
]

ADMIN_ROUTES = [
    f"/admin/{SLUG}/dashboard",     # BI e Métricas
    f"/admin/{SLUG}/menu",          # Engenharia de Cardápio
    f"/admin/{SLUG}/tables",        # Gestão de Mesas
    f"/admin/{SLUG}/inventory",     # Estoque
    f"/admin/{SLUG}/marketing",     # IA e Fidelidade
    f"/admin/{SLUG}/team",          # Equipe
    f"/admin/{SLUG}/history",       # Histórico
    f"/admin/{SLUG}/settings",      # Configurações
    f"/admin/{SLUG}/kitchen",       # KDS
    f"/admin/{SLUG}/waiter",        # App do Garçom
    f"/admin/{SLUG}/delivery",      # Despacho
]

def open_tabs():
    print("🚀 Iniciando Auditoria Visual Inteligente...")
    
    # FASE 1: Autenticação
    print("\n🔑 FASE 1: Autenticação")
    print(f"Abrindo tela de login: {AUTH_ROUTE}")
    webbrowser.open(f"{BASE_URL}{AUTH_ROUTE}")
    
    print("\n" + "!"*50)
    print("PAUSA OBRIGATÓRIA:")
    print("1. Vá ao navegador e faça o login (admin@mesaflow.com / 123456).")
    print("2. Após estar logado no Dashboard, volte aqui.")
    print("!"*50)
    
    input("\n👉 Pressione ENTER aqui no terminal para abrir as outras telas...")

    # FASE 2: Telas Públicas
    print("\n🌍 FASE 2: Abrindo Telas Públicas...")
    for route in PUBLIC_ROUTES:
        print(f"  [OK] {route}")
        webbrowser.open(f"{BASE_URL}{route}")
        time.sleep(0.3)

    # FASE 3: Telas Administrativas (Já autenticadas)
    print("\n📊 FASE 3: Abrindo Telas de Gestão...")
    for route in ADMIN_ROUTES:
        print(f"  [OK] {route}")
        webbrowser.open(f"{BASE_URL}{route}")
        time.sleep(0.3)

    print("\n" + "="*50)
    print("✨ Concluído! Todas as telas foram carregadas.")
    print("Se alguma tela ainda pedir login, verifique se você logou na aba correta.")
    print("="*50)

if __name__ == "__main__":
    try:
        open_tabs()
    except KeyboardInterrupt:
        print("\n🛑 Cancelado pelo usuário.")
