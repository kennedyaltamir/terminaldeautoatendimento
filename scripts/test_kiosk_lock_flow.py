# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 21:25:00
import pytest
import re
from playwright.async_api import Page, expect

# ==============================================================================
# 🛡️ KIOSK LOCK FLOW TEST (L6 - Async Hardened)
# ==============================================================================
# Fix: Removido qualquer uso de asyncio.run() ou Runner.run().
# O ciclo de vida do loop é gerenciado inteiramente pelo pytest-asyncio.
# ==============================================================================

BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"

@pytest.mark.asyncio
async def test_01_enter_kiosk_mode(page: Page):
    """Valida a entrada no modo totem e ocultação do botão de ativação."""
    await page.goto(f"{BASE_URL}/{SLUG}/kiosk")
    await page.evaluate("localStorage.setItem('mesaflow_kiosk_state', 'IDLE')")
    await page.reload()
    
    enter_btn = page.get_by_text("ATIVAR MODO TOTEM")
    await expect(enter_btn).toBeVisible()
    await enter_btn.click()
    await expect(enter_btn).not_to_be_visible()

@pytest.mark.asyncio
async def test_02_unauthorized_exit_attempt(page: Page):
    """Valida que a saída do fullscreen sem senha dispara o modal de violação."""
    await page.goto(f"{BASE_URL}/{SLUG}/kiosk")
    await page.evaluate("localStorage.setItem('mesaflow_kiosk_state', 'LOCKED')")
    await page.reload()
    
    # Simula violação de fullscreen via evento de DOM
    await page.evaluate("document.dispatchEvent(new Event('fullscreenchange'))")
    modal = page.locator(".fixed.inset-0")
    await expect(modal).toBeVisible()

@pytest.mark.asyncio
async def test_03_password_validation_flow(page: Page):
    """Valida o fluxo de senha (erro e sucesso) no modo Kiosk."""
    await page.goto(f"{BASE_URL}/{SLUG}/kiosk")
    await page.evaluate("localStorage.setItem('mesaflow_kiosk_state', 'BREACHED')")
    await page.reload()
    
    # Senha Errada
    for char in "123":
        await page.get_by_text(char, exact=True).first.click()
    
    # Localiza botão de confirmação por texto flexível (Restaurar/Desbloquear)
    confirm_btn = page.locator("button").filter(has_text=re.compile("Restaurar|Desbloquear|Confirmar", re.I)).first
    await confirm_btn.click()
    await expect(page.get_by_text(re.compile("SENHA INCORRETA", re.I))).toBeVisible()
    
    # Senha Certa (Default: 123456)
    # Limpa entrada anterior via botão DEL
    del_btn = page.locator("button").filter(has=page.locator("svg.lucide-delete")).first
    if await del_btn.is_visible():
        for _ in range(3): await del_btn.click()
        
    for char in "123456":
        await page.get_by_text(char, exact=True).first.click()
    await confirm_btn.click()
    
    # Modal deve sumir
    await expect(page.locator(".fixed.inset-0")).not_to_be_visible()

