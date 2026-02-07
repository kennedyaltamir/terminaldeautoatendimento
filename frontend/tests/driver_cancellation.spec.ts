import { test, expect } from '@playwright/test';

test.use({ 
  headless: false, 
  viewport: { width: 390, height: 844 }, 
  launchOptions: { slowMo: 600 } 
});

test.describe('Logistics: Cancellation Rito with Confirmation', () => {

  test('Deve aceitar missão e cancelar com sucesso', async ({ page, context }) => {
    await context.grantPermissions(['geolocation']);
    await context.setGeolocation({ latitude: -23.5505, longitude: -46.6333 });
    
    await page.goto('/admin/hamburgueria-ze/driver');

    // 🛡️ PASSO 0: Forçar aba MISSION (Rota)
    const missionTab = page.locator('button').filter({ has: page.locator('svg.lucide-map') });
    await missionTab.click();

    // 1. Iniciar Turno
    const startBtn = page.locator('button:has-text("Iniciar Trabalho")');
    if (await startBtn.isVisible()) await startBtn.click();

    // 2. Aceitar Rota (Pressão Longa)
    const acceptBtn = page.locator('text=ACEITAR ROTA').first();
    await expect(acceptBtn).toBeVisible({ timeout: 15000 });
    const acceptBox = await acceptBtn.boundingBox();
    if (acceptBox) {
      await page.mouse.move(acceptBox.x + acceptBox.width / 2, acceptBox.y + acceptBox.height / 2);
      await page.mouse.down();
      await page.waitForTimeout(3500); 
      await page.mouse.up();
    }

    // 3. Rito de Iniciar Rota (Segurar)
    const deck = page.getByTestId('control-deck-container');
    await deck.scrollIntoViewIfNeeded();

    const startNavBtn = page.getByTestId('btn-start-navigation');
    const navBox = await startNavBtn.boundingBox();
    if (navBox) {
      await page.mouse.move(navBox.x + navBox.width / 2, navBox.y + navBox.height / 2);
      await page.mouse.down();
      await page.waitForTimeout(3500); 
      await page.mouse.up();
    }

    // 4. Verificar Navegação e Cancelar
    await expect(page.locator('text=Cheguei no Local')).toBeVisible({ timeout: 10000 });
    
    console.log('🛑 Solicitando cancelamento...');
    const cancelBtn = page.getByTestId('btn-cancel-mission');
    await cancelBtn.click();

    // 5. Validar Modal de Confirmação
    await expect(page.locator('text=Deseja realmente cancelar')).toBeVisible({ timeout: 5000 });
    await page.locator('button:has-text("CANCELAR")').click();

    // 6. Validar Retorno ao Estado IDLE
    await expect(page.locator('text=Buscando Missões').or(page.locator('text=ACEITAR ROTA').first())).toBeVisible({ timeout: 15000 });
  });
});
