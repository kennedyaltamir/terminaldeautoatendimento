// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 19:25:00
import { test, expect } from '@playwright/test';

/**
 * Testes de Logística E2E
 * A autenticação é gerenciada globalmente pelo storageState definido no config.
 */

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    // Agora o sistema não redireciona mais para /login pois os cookies/storage já estão injetados
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // Identifica o card
    const card = page.getByTestId('driver.delivery.order.card').first();
    await expect(card).toBeVisible({ timeout: 15000 });
    
    // Inicia coleta
    await card.getByTestId('driver.delivery.order.pickup').click();
    
    // Valida transição para modo navegação
    await expect(page.getByTestId('driver.delivery.active')).toBeVisible({ timeout: 10000 });
});

test('Test 10: Client Passive Tracking', async ({ page }) => {
    // Regra Arquitetural: Cliente é passivo
    page.on('request', req => {
        if (req.url().includes('osrm') || req.url().includes('google.com/maps/dir')) {
            throw new Error('VIOLAÇÃO: Cliente tentando calcular rota localmente!');
        }
    });

    // 1. Obtém um pedido ativo para visualização
    await page.goto('/admin/hamburgueria-ze/driver');
    const card = page.getByTestId('driver.delivery.order.card').first();
    const orderId = await card.getAttribute('data-order-id');

    // 2. Navega para a visão do cliente
    await page.goto(`/hamburgueria-ze/menu?order=${orderId}`);
    
    // 3. Valida renderização da UI de acompanhamento
    await expect(page.locator('h1')).toContainText('Olá');
});
