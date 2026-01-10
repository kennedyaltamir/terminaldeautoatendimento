import pytest
import json
import re
import socket
import logging
import os
import time
from playwright.sync_api import Page, expect

# Configuração de Logging de Nível Industrial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("E2E-ULTRA-RIGIDO")

SCREENSHOT_PATH = "debug_screenshots"
if not os.path.exists(SCREENSHOT_PATH):
    os.makedirs(SCREENSHOT_PATH)

def is_frontend_running(host="127.0.0.1", port=3000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

@pytest.fixture(scope="session", autouse=True)
def pre_flight_check():
    logger.info("🔍 [PRE-FLIGHT] Verificando infraestrutura...")
    if not is_frontend_running():
        msg = "❌ FRONTEND OFFLINE. Rode 'npm run dev' na pasta frontend."
        logger.error(msg)
        pytest.exit(msg)

@pytest.fixture(autouse=True)
def setup_promotion_mocks(page: Page):
    # Espelhamento de Console
    page.on("console", lambda msg: logger.info(f"🌐 [BROWSER] {msg.text}"))
    
    def handle_menu(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "company": {"name": "Loja de Teste", "primary_color": "#ea580c"},
                "categories": [{
                    "id": 1, "name": "Lanches",
                    "products": [{
                        "id": 100, "name": "Hambúrguer Teste", "price": 50.00,
                        "is_available": True, "track_stock": False, "tags": ["promo"],
                        "option_groups": [{
                            "id": 1, "name": "Ponto", "min_selection": 1, "max_selection": 1,
                            "options": [{"id": 1, "name": "Bem Passado", "price": 0}]
                        }]
                    }]
                }]
            })
        )

    def handle_coupon(route):
        payload = route.request.post_data_json
        if payload.get("code") == "TESTE10":
            route.fulfill(
                status=200, content_type="application/json",
                body=json.dumps({
                    "valid": True, "discount_amount": 10.00, "final_total": 40.00,
                    "message": "Cupom OK", "promotion_id": "uuid-123"
                })
            )
        else:
            route.fulfill(status=400, body=json.dumps({"detail": "Invalido"}))

    page.route("**/api/*/menu", handle_menu)
    page.route("**/api/*/cart/validate-coupon", handle_coupon)
    page.goto("http://localhost:3000/hamburgueria-ze/menu", wait_until="networkidle")

def test_apply_valid_coupon(page: Page):
    logger.info("🧪 [TEST] Sucesso de Cupom")
    page.get_by_text("Hambúrguer Teste").click()
    page.get_by_text("Bem Passado").click()
    page.get_by_role("button", name=re.compile("Adicionar", re.I)).click()
    page.get_by_role("button", name=re.compile("Ver Carrinho", re.I)).click()
    
    page.get_by_placeholder("CÓDIGO").fill("TESTE10")
    page.get_by_role("button", name="Aplicar").click()

    expect(page.get_by_text("- R$ 10.00")).to_be_visible()
    expect(page.get_by_text("R$ 40.00")).to_be_visible()
    logger.info("✅ Sucesso validado.")

def test_apply_invalid_coupon(page: Page):
    logger.info("🧪 [TEST] Erro de Cupom")
    page.get_by_text("Hambúrguer Teste").click()
    page.get_by_text("Bem Passado").click()
    page.get_by_role("button", name=re.compile("Adicionar", re.I)).click()
    page.get_by_role("button", name=re.compile("Ver Carrinho", re.I)).click()

    page.get_by_placeholder("CÓDIGO").fill("ERRADO")
    page.get_by_role("button", name="Aplicar").click()

    expect(page.get_by_text("Invalido")).to_be_visible()
    logger.info("✅ Erro validado.")

def test_remove_discount_on_cart_change(page: Page):
    logger.info("🧪 [TEST] Invalidação por Mudança (MODO RÍGIDO)")
    
    # 1. Setup do estado
    page.get_by_text("Hambúrguer Teste").click()
    page.get_by_text("Bem Passado").click()
    page.get_by_role("button", name=re.compile("Adicionar", re.I)).click()
    page.get_by_role("button", name=re.compile("Ver Carrinho", re.I)).click()
    page.get_by_placeholder("CÓDIGO").fill("TESTE10")
    page.get_by_role("button", name="Aplicar").click()
    
    # Garante que o desconto está lá
    expect(page.get_by_text("- R$ 10.00")).to_be_visible()
    
    logger.info("🗑️ Disparando remoção via Injeção de Script (Bypass de UI)...")
    
    # 2. Ação Rígida: Força o clique via JS para evitar problemas de scroll/interceptação
    remover_locator = page.get_by_role("button", name="Remover").first
    remover_locator.evaluate("node => node.click()")
    
    # 3. Sincronização de Estado (Espera o desconto sumir do DOM)
    logger.info("⏳ Aguardando limpeza de estado no React...")
    try:
        page.wait_for_function(
            "() => !document.body.innerText.includes('- R$ 10.00')",
            timeout=5000
        )
    except Exception:
        page.screenshot(path=f"{SCREENSHOT_PATH}/fail_state_sync.png")
        logger.error(f"❌ O desconto não sumiu. HTML atual: {page.content()[:500]}")
        raise

    # 4. Validação Final
    logger.info("✨ Validando mensagem de alerta...")
    # Usamos um seletor de texto parcial e flexível
    expect(page.get_by_text(re.compile("Carrinho alterado", re.I))).to_be_visible(timeout=5000)
    
    page.screenshot(path=f"{SCREENSHOT_PATH}/final_success_rigid.png")
    logger.info("✅ [PASS] Invalidação confirmada com sucesso.")
