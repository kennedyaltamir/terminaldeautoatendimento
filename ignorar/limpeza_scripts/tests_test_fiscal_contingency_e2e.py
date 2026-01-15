import pytest
import json
import re
import socket
import logging
import os
import time
from playwright.sync_api import Page, expect

# Configuração de Logging Rígido
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("E2E-FISCAL-OFFLINE")

SCREENSHOT_PATH = "debug_screenshots"
if not os.path.exists(SCREENSHOT_PATH):
    os.makedirs(SCREENSHOT_PATH)

def is_frontend_running(host="127.0.0.1", port=3000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

@pytest.fixture(scope="session", autouse=True)
def pre_flight_check():
    logger.info("🔍 [PRE-FLIGHT] Verificando ambiente...")
    if not is_frontend_running():
        msg = "❌ FRONTEND OFFLINE. Rode 'npm run dev' na pasta frontend."
        logger.error(msg)
        pytest.exit(msg)

@pytest.fixture(autouse=True)
def setup_fiscal_mocks(page: Page):
    """Configura o ambiente blindado contra modais e com dados de teste."""
    
    # Mock do Histórico com um pedido pendente
    def handle_history(route):
        # Captura se o status já mudou para emitted no servidor (simulado)
        # Para o teste de sync, o primeiro fetch retorna pending, o segundo emitted.
        status = "pending"
        if "emitted_flag" in page.url: status = "emitted"

        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "total": 1, "page": 1, "limit": 10,
                "data": [{
                    "id": "order-cont-123",
                    "customer_name": "Cliente Contingencia",
                    "total_amount": 150.00,
                    "status": "delivered",
                    "payment_status": "paid",
                    "fiscal_status": status,
                    "nfe_url_pdf": "https://mesaflow.com.br/nfe/123.pdf" if status == "emitted" else None,
                    "created_at": "2026-01-05T20:00:00Z",
                    "table": {"table_number": 10}
                }]
            })
        )

    # Mock da Emissão (Sucesso)
    def handle_emit(route):
        logger.info("📡 [API] Recebida solicitação de emissão pós-contingência!")
        # Simula a mudança de estado no "servidor" para o próximo fetch
        page.goto(page.url + "#emitted_flag") 
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"status": "success", "message": "Nota emitida"})
        )

    page.route("**/api/admin/*/history*", handle_history)
    page.route("**/api/admin/fiscal/orders/*/emit", handle_emit)
    
    page.context.add_init_script("""
        localStorage.setItem('mesaflow_access_token', 'fake-admin-token');
        localStorage.setItem('mesaflow_user_role', 'owner');
        localStorage.setItem('mesaflow_tour_completed', 'true');
    """)

    page.goto("http://localhost:3000/admin/hamburgueria-ze/history", wait_until="networkidle")
    page.evaluate("() => { const tour = document.getElementById('react-joyride-portal'); if(tour) tour.remove(); }")

def test_fiscal_offline_contingency_flow(page: Page):
    logger.info("🧪 Iniciando Teste de Contingência Fiscal Offline")

    # 1. OFFLINE
    logger.info("🔌 Cortando conexão...")
    page.context.set_offline(True)
    
    btn_emitir = page.locator("button:has-text('Emitir Nota')").first
    btn_emitir.click(force=True)

    # 2. VALIDAR FILA
    expect(page.get_by_text(re.compile("Na Fila", re.I))).to_be_visible(timeout=10000)
    expect(page.get_by_text(re.compile("Notas em Contingência", re.I))).to_be_visible()
    logger.info("✅ Nota em fila local.")

    # 3. ONLINE
    logger.info("🌐 Restaurando conexão...")
    page.context.set_offline(False)
    
    # Pequena espera para o navegador disparar o evento 'online'
    page.wait_for_timeout(2000)

    # 4. VALIDAR SYNC E REFRESH
    logger.info("⏳ Aguardando sincronização e refresh da UI...")
    
    # O badge deve mudar para "NFC-e" após o refresh automático da página
    badge_sucesso = page.locator("a:has-text('NFC-e')")
    expect(badge_sucesso).to_be_visible(timeout=20000)
    
    expect(page.get_by_text(re.compile("Notas em Contingência", re.I))).not_to_be_visible()
    logger.info("✅ Sincronização e Refresh validados.")

def test_fiscal_error_handling_in_queue(page: Page):
    logger.info("🧪 Iniciando Teste de Erro na Fila")
    
    page.route("**/api/admin/fiscal/orders/*/emit", lambda route: route.fulfill(
        status=400,
        body=json.dumps({"detail": "Erro Fiscal Simulado"})
    ))

    page.context.set_offline(True)
    page.locator("button:has-text('Emitir Nota')").first.click(force=True)
    
    page.context.set_offline(False)
    page.wait_for_timeout(2000)

    # Deve mostrar "Erro na Fila" e o indicador global deve ficar vermelho
    badge_erro = page.get_by_text(re.compile("Erro na Fila", re.I))
    expect(badge_erro).to_be_visible(timeout=15000)
    
    logger.info("✅ Tratamento de erro validado.")
