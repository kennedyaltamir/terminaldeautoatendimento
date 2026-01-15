// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 14:40:00
import { test, expect } from '@playwright/test';

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    await page.goto('/admin/hamburgueria-ze/driver');
    
    const card = page.getByTestId('driver.delivery.order.card').first();
    await expect(card).toBeVisible({ timeout: 15000 });
    
    // 1. Prepara a captura da resposta da API
    const responsePromise = page.waitForResponse(resp => 
        resp.url().includes('/dispatch') && resp.status() === 200
    );

    // 2. Clica no botão de pickup
    await card.getByTestId('driver.delivery.order.pickup').click({ force: true });
    
    // 3. Aguarda a confirmação do servidor antes de validar a UI
    await responsePromise;

    // 4. Valida a transição para o modo de mapa
    await expect(page.getByTestId('driver.delivery.active')).toBeVisible({ timeout: 15000 });
});
