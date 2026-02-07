// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 13:35:00
import { test, expect } from '@playwright/test';

test.describe('Kiosk Lock Security', () => {
  
  test('Deve ativar o modo Kiosk e persistir no reload', async ({ page }) => {
    await page.goto('/hamburgueria-ze/kiosk');
    
    // 1. Ativar via botão visível (IDLE state)
    const activateBtn = page.getByText('ATIVAR MODO TOTEM');
    await expect(activateBtn).toBeVisible();
    await activateBtn.click();
    
    // 2. Verificar Toast
    await expect(page.getByText('Modo Totem Ativado')).toBeVisible();
    
    // 3. Verificar desaparecimento do botão (Stealth Mode)
    await expect(activateBtn).not.toBeVisible();
    
    // 4. Reload
    await page.reload();
    
    // 5. Verificar persistência (Botão ainda invisível)
    await expect(activateBtn).not.toBeVisible();
  });

  test('Deve acionar o Trap Mode ao sair do fullscreen forçadamente', async ({ page }) => {
    // Setup: Estado Locked
    await page.addInitScript(() => {
      localStorage.setItem('mesaflow_kiosk_state', 'LOCKED');
    });
    await page.goto('/hamburgueria-ze/kiosk');

    // Simular evento de saída de fullscreen
    await page.evaluate(() => {
      document.dispatchEvent(new Event('fullscreenchange'));
    });

    // Verificar Modal de Violação (Vermelho)
    const modal = page.locator('text=SISTEMA VIOLADO');
    await expect(modal).toBeVisible();
    
    // Verificar ausência de botão Cancelar
    await expect(page.getByText('Cancelar')).not.toBeVisible();
  });

  test('Deve desbloquear com a senha correta', async ({ page }) => {
    // Setup: Estado Breached
    await page.addInitScript(() => {
      localStorage.setItem('mesaflow_kiosk_state', 'BREACHED');
    });
    await page.goto('/hamburgueria-ze/kiosk');

    // Digitar senha padrão
    await page.getByText('1').click();
    await page.getByText('2').click();
    await page.getByText('3').click();
    await page.getByText('4').click();
    await page.getByText('5').click();
    await page.getByText('6').click();
    
    await page.getByText('RESTAURAR SISTEMA').click();

    // Verificar desbloqueio
    await expect(page.getByText('Modo Administrativo Liberado')).toBeVisible();
    await expect(page.getByText('ATIVAR MODO TOTEM')).toBeVisible(); // Voltou para IDLE
  });
});

