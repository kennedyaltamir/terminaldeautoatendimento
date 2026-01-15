// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 18:30:00
import { test, expect } from '@playwright/test';

/**
 * Test 9: Transição do Dashboard para o Mapa
 * Valida o "Modo Navegação" do entregador.
 */
test('Test 9: Driver Transitions to Map', async ({ page }) => {
    // Nota: O slug deve ser o mesmo do seed
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // Identifica o card pelo testid padrão L6
    const card = page.locator('[data-testid="driver.delivery.order.card"]').first();
    
    // Clica no botão de pickup
    await card.locator('[data-testid="driver.delivery.order.pickup"]').click();
    
    // Valida que a UI mudou para o modo ativo (Navegação)
    await expect(page.locator('[data-testid="driver.delivery.active"]')).toBeVisible();
});

/**
 * Test 10: Rastreamento Passivo do Cliente
 * Garante que o cliente não consome recursos de rota.
 */
test('Test 10: Client Passive Tracking', async ({ page }) => {
    // Listener de rede para capturar vazamentos de lógica (calculando rota no cliente)
    page.on('request', req => {
        if (req.url().includes('osrm') || req.url().includes('google.com/maps/dir')) {
            throw new Error('VIOLAÇÃO: Cliente tentando calcular rota localmente!');
        }
    });

    // Simula visualização de um pedido específico
    await page.goto('/hamburgueria-ze/menu?order=any-active-id');
    
    // Verifica se o mapa carregou
    await expect(page.locator('[data-testid="customer.order.map"]')).toBeAttached();
});
