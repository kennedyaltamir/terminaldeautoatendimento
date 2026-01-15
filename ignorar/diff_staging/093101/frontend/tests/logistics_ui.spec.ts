// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 19:30:00
import { test, expect } from '@playwright/test';

/**
 * 🧪 Testes de Logística E2E (L6 - Hardened)
 * 
 * NOTA DE GOVERNANÇA: A autenticação é herdada globalmente do storageState.
 * NÃO use beforeEach para injetar localStorage manualmente aqui, pois isso
 * sobrescreve a sessão real gerada pelo setup.
 */

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // Identifica o card pelo TestID padrão MesaFlow
    const card = page.getByTestId('driver.delivery.order.card').first();
    
    // Aguarda visibilidade (ajudado pela remoção do overlay do Joyride no setup)
    await expect(card).toBeVisible({ timeout: 15000 });
    
    // Clica no botão de pickup
    await card.getByTestId('driver.delivery.order.pickup').click();
    
    // Valida transição para modo navegação ativa
    await expect(page.getByTestId('driver.delivery.active')).toBeVisible({ timeout: 10000 });
});

test('Test 10: Client Passive Tracking', async ({ page }) => {
    // Interceptação de rede para garantir conformidade arquitetural (Cliente Passivo)
    page.on('request', req => {
        const url = req.url();
        if (url.includes('osrm') || url.includes('google.com/maps/dir')) {
            throw new Error(`VIOLAÇÃO ARQUITETURAL: Cliente calculando rota localmente! URL: ${url}`);
        }
    });

    // 1. Obtém um pedido da lista do entregador
    await page.goto('/admin/hamburgueria-ze/driver');
    const card = page.getByTestId('driver.delivery.order.card').first();
    await expect(card).toBeVisible();
    const orderId = await card.getAttribute('data-order-id');

    // 2. Navega para a visão do cliente
    await page.goto(`/hamburgueria-ze/menu?order=${orderId}`);
    
    // 3. Valida renderização da UI de status
    await expect(page.locator('h1')).toContainText('Olá');
    await expect(page.getByTestId('customer.order.stepper')).toBeVisible();
});
