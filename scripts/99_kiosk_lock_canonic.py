# DOMAIN: DEVOPS_SCRIPTS
# TEST: KIOSK_LOCK_FLOW
# VERSION: 2.6 (Pytest-Asyncio Compliant)
# LAST_MODIFIED: 2026-01-16 19:48:00
import pytest
import re
from playwright.async_api import Page, expect

BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
KIOSK_ROUTE = re.compile(".*/kiosk")
ADMIN_ROUTE = re.compile(".*/admin/login")

@pytest.mark.asyncio
async def test_kiosk_lock_flow_v2(page: Page):
    """
    Valida o isolamento de segurança do modo Kiosk e previne fugas para rotas administrativas.
    """
    print("🔒 Iniciando Teste de Fluxo de Bloqueio Kiosk (v2.6)")
    
    # 1. Acesso ao Kiosk
    await page.goto(f"{BASE_URL}/{SLUG}/kiosk")
    await page.wait_for_load_state("networkidle")
    await expect(page).to_have_url(KIOSK_ROUTE)

    # 2. Ativar Modo Totem (Fullscreen Toggle)
    activate_btn = page.get_by_text("ATIVAR MODO TOTEM")
    if await activate_btn.is_visible():
        await activate_btn.click()
    else:
        # Trigger Manual se o botão estiver oculto por estado persistente
        await page.evaluate("localStorage.setItem('mesaflow_kiosk_state', 'LOCKED')")
        await page.reload()
    
    # 3. Modal de Desbloqueio deve aparecer
    modal = page.locator(".fixed.inset-0")
    await expect(modal).to_be_visible(timeout=5000)
    
    # 4. Testar Senha Incorreta
    confirm_btn = page.get_by_test_id("kiosk-unlock-confirm")
    for num in "123":
        await page.get_by_text(num, exact=True).first.click()
    await confirm_btn.click()
    
    # 5. Validação de Segurança (Não deve redirecionar)
    await expect(modal).to_be_visible()
    assert not ADMIN_ROUTE.match(page.url), "ERRO: O sistema redirecionou para login administrativo após falha de senha no Kiosk."

    # 6. Testar Senha Correta (Default: 123456)
    # Limpa entrada anterior
    del_btn = page.locator("button").filter(has=page.locator("svg.lucide-delete")).first
    if await del_btn.is_visible():
        for _ in range(3): await del_btn.click()
        
    for num in "123456":
        await page.get_by_text(num, exact=True).first.click()
    await confirm_btn.click()
    
    # 7. Validar Desbloqueio
    await expect(modal).not_to_be_visible(timeout=5000)
    print("✅ Fluxo de bloqueio validado com sucesso.")

