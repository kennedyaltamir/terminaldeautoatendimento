// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 18:10:00
import { test, expect } from '@playwright/test';

/**
 * 🛡️ Setup de Autenticação para Testes Administrativos
 * Injeta o token diretamente no localStorage para evitar redirecionamento para /login.
 */
test.beforeEach(async ({ page }) => {
    // 1. Navega para a raiz para estabelecer o domínio do localStorage
    await page.goto('/');
    
    // 2. Injeta estado de sessão autenticada (Admin Mock)
    await page.evaluate(() => {
        // Nota: O token abaixo é sintático para passar pelo middleware do frontend
        const fakeToken = "header.eyJzdWIiOiJhZG1pbkBtZXNhZmxvdy5jb20iLCJyb2xlIjoib3duZXIiLCJjb21wYW55X2lkIjoiZGVkNDUyYWYtNmM2My00YTYyLWIwMmEtZDA3ZGEzNDQ1M2UxIn0.signature";
        localStorage.setItem('mesaflow_access_token', fakeToken);
        localStorage.setItem('mesaflow_user_role', 'owner');
        localStorage.setItem('mesaflow_tour_completed', 'true');
    });
});

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    // Acessa diretamente a página do entregador (já autenticado via beforeEach)
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // Localiza o card pelo testid padrão
    const card = page.locator('[data-testid="driver.delivery.order.card"]').first();
    await expect(card).toBeVisible({ timeout: 15000 });
    
    // Clica no botão de pickup
    await card.locator('[data-testid="driver.delivery.order.pickup"]').click();
    
    // Valida que a UI mudou para o modo ativo (Navegação)
    await expect(page.locator('[data-testid="driver.delivery.active"]')).toBeVisible({ timeout: 10000 });
});

test('Test 10: Client Passive Tracking', async ({ page }) => {
    // Monitor de rede para garantir que o cliente não recalcula a rota
    page.on('request', req => {
        if (req.url().includes('osrm') || req.url().includes('google.com/maps/dir')) {
            throw new Error('VIOLAÇÃO: Cliente tentando calcular rota localmente!');
        }
    });

    // 1. Obtém ID de um pedido existente na tela do entregador
    await page.goto('/admin/hamburgueria-ze/driver');
    const card = page.locator('[data-testid="driver.delivery.order.card"]').first();
    const orderId = await card.getAttribute('data-order-id');

    // 2. Navega para a visão do cliente com o ID real
    await page.goto(`/hamburgueria-ze/menu?order=${orderId}`);
    
    // 3. Verifica se a interface de acompanhamento montou (Olá Cliente)
    await expect(page.locator('h1')).toContainText('Olá');
});
