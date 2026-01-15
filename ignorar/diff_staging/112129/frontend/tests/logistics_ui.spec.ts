// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 15:25:00
import { test, expect } from '@playwright/test';

test.describe.configure({ mode: 'serial' });

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // 1. Aguarda a hidratação da página e a primeira carga da API
    const card = page.getByTestId('driver.delivery.order.card').first();
    
    // Aumentado timeout para 30s devido à latência observada nos logs (2.2s por request)
    await expect(card).toBeVisible({ 
        timeout: 30000,
        message: "FALHA: O pedido semeado não apareceu na lista. Verifique o Redis e o RLS."
    });
    
    const dispatchPromise = page.waitForResponse(resp => 
        resp.url().includes('/dispatch') && resp.status() === 200
    );

    await card.getByTestId('driver.delivery.order.pickup').click({ force: true });
    await dispatchPromise;

    await expect(page.getByTestId('driver.delivery.active')).toBeVisible({ timeout: 15000 });
});
