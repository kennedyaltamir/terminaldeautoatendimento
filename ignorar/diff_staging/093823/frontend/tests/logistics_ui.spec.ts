// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 19:45:00
import { test, expect } from '@playwright/test';

/**
 * 🧪 Testes de Logística E2E (L6 - Hardened)
 * 
 * NOTA DE GOVERNANÇA: A autenticação é herdada globalmente do storageState.
 * O setup em auth.setup.ts injeta 'mesaflow_tour_completed' para evitar bloqueios.
 */

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // 1. Localiza o card de pedido disponível
    const card = page.getByTestId('driver.delivery.order.card').first();
    await expect(card).toBeVisible({ timeout: 15000 });
    
    // 2. Prepara a captura da resposta de rede para evitar race conditions
    const dispatchPromise = page.waitForResponse(resp => 
        resp.url().includes('/dispatch') && resp.status() === 200
    );

    // 3. Executa o pickup
    // force: true ignora interceptações de ponteiro (ex: overlays de tour)
    await card.getByTestId('driver.delivery.order.pickup').click({ force: true });
    
    // 4. Aguarda confirmação do backend
    await dispatchPromise;

    // 5. Valida transição para modo navegação ativa
    // Aumentado timeout para 15s para suportar carregamento do mapa Leaflet
    await expect(page.getByTestId('driver.delivery.active')).toBeVisible({ timeout: 15000 });
});

test('Test 10: Client Passive Tracking', async ({ page }) => {
    // Interceptação de rede para garantir conformidade arquitetural (Cliente Passivo)
    page.on('request', req => {
        const url = req.url();
        if (url.includes('osrm') || url.includes('google.com/maps/dir')) {
            throw new Error(`VIOLAÇÃO ARQUITETURAL: Cliente calculando rota localmente! URL: ${url}`);
        }
    });

    // 1. Obtém um pedido da lista do entregador para rastreio
    await page.goto('/admin/hamburgueria-ze/driver');
    const card = page.getByTestId('driver.delivery.order.card').first();
    await expect(card).toBeVisible();
    const orderId = await card.getAttribute('data-order-id');

    // 2. Navega para a visão do cliente
    await page.goto(`/hamburgueria-ze/menu?order=${orderId}`);
    
    // 3. Valida renderização da UI de status e stepper
    await expect(page.locator('h1')).toContainText('Olá');
    await expect(page.getByTestId('customer.order.stepper')).toBeVisible();
});
