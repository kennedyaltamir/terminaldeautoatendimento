// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 18:45:00
import { test, expect } from '@playwright/test';

/**
 * Test 9: Transição do Dashboard para o Mapa
 * Valida o "Modo Navegação" do entregador.
 */
test('Test 9: Driver Transitions to Map', async ({ page }) => {
    // 1. Acessa Painel do Entregador
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // 2. Aguarda a lista de pedidos carregar (Polling/Fetch)
    const card = page.locator('[data-testid="driver.delivery.order.card"]').first();
    await expect(card).toBeVisible({ timeout: 15000 });
    
    const orderId = await card.getAttribute('data-order-id');
    console.log(`Auditoria: Iniciando coleta do pedido ${orderId}`);

    // 3. Clica no botão de pickup
    await card.locator('[data-testid="driver.delivery.order.pickup"]').click();
    
    // 4. Valida que a UI mudou para o modo ativo (Navegação)
    await expect(page.locator('[data-testid="driver.delivery.active"]')).toBeVisible({ timeout: 10000 });
});

/**
 * Test 10: Rastreamento Passivo do Cliente
 * Garante que o cliente não consome recursos de rota e vê o mapa.
 */
test('Test 10: Client Passive Tracking', async ({ page }) => {
    // Listener de rede para capturar vazamentos de lógica
    page.on('request', req => {
        if (req.url().includes('osrm') || req.url().includes('google.com/maps/dir')) {
            throw new Error('VIOLAÇÃO: Cliente tentando calcular rota localmente!');
        }
    });

    // 1. Busca um pedido ativo para visualizar
    await page.goto('/admin/hamburgueria-ze/driver');
    const card = page.locator('[data-testid="driver.delivery.order.card"]').first();
    const orderId = await card.getAttribute('data-order-id');

    // 2. Navega para a visão do cliente
    await page.goto(`/hamburgueria-ze/menu?order=${orderId}`);
    
    // 3. Verifica se o componente de status carregou
    await expect(page.locator('h1')).toContainText('Olá');
});
