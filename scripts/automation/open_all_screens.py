# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 02:35:00
import webbrowser
import time
import sys

# Configurações Base
BASE_URL = "http://localhost:3000"
DEFAULT_SLUG = "hamburgueria-ze"

# Mapeamento de Rotas baseado na estrutura do App Router
ROUTES = [
    "/",                                      # Landing Page
    "/admin/login",                           # Login Admin
    "/admin/register",                        # Registro de Empresa
    "/admin/forgot-password",                 # Recuperação de Senha
    "/admin/support",                         # God Mode / Suporte
    f"/{DEFAULT_SLUG}/menu",                  # Cardápio Público (PWA)
    f"/{DEFAULT_SLUG}/kiosk",                 # Modo Totem (Kiosk)
    f"/admin/{DEFAULT_SLUG}/dashboard",       # Dashboard de BI
    f"/admin/{DEFAULT_SLUG}/kitchen",         # Monitor de Cozinha (KDS)
    f"/admin/{DEFAULT_SLUG}/waiter",          # App do Garçom (Mesas)
    f"/admin/{DEFAULT_SLUG}/delivery",        # Gestão de Logística
    f"/admin/{DEFAULT_SLUG}/counter",         # PDV de Balcão
    f"/admin/{DEFAULT_SLUG}/settings",        # Configurações Gerais
    f"/admin/{DEFAULT_SLUG}/inventory",       # Gestão de Estoque
    f"/admin/{DEFAULT_SLUG}/menu",            # Engenharia de Cardápio
    f"/admin/{DEFAULT_SLUG}/tables",          # Gestão de Mesas/QR Codes
    f"/admin/{DEFAULT_SLUG}/marketing",       # Marketing & IA
    f"/admin/{DEFAULT_SLUG}/team",            # Gestão de Equipe
    f"/admin/{DEFAULT_SLUG}/history",         # Histórico de Pedidos
    f"/admin/{DEFAULT_SLUG}/audit",           # Logs de Auditoria
    f"/admin/{DEFAULT_SLUG}/franchise",       # Dashboard de Franquia
    "/trust",                                 # Trust Center Index
    "/trust/status",                          # Status Page
    "/trust/security"                         # Security & Compliance
]

def open_screens():
    print("🚀 MesaFlow Screen Orchestrator v1.0")
    print("======================================")
    print(f"Base URL: {BASE_URL}")
    print(f"Slug Alvo: {DEFAULT_SLUG}")
    print(f"Total de telas: {len(ROUTES)}")
    print("======================================")
    
    confirm = input("Deseja abrir todas as abas no seu navegador padrão? (s/N): ").strip().lower()
    if confirm not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada.")
        return

    for i, route in enumerate(ROUTES):
        url = f"{BASE_URL}{route}"
        print(f"[{i+1}/{len(ROUTES)}] Abrindo: {url}")
        webbrowser.open(url)
        # Pequeno delay para não sobrecarregar o navegador/CPU
        time.sleep(0.3)

    print("\n✨ Todas as telas foram solicitadas ao navegador.")
    print("Dica: Certifique-se de que o 'python run.py' está rodando.")

if __name__ == "__main__":
    open_screens()
