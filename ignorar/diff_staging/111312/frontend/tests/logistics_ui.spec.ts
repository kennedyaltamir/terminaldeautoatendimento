// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 15:00:00
import { test, expect } from '@playwright/test';

/**
 * 🧪 Testes de Logística E2E (L6 - Hardened)
 * MODO SERIAL: Obrigatório para evitar colisões de estado no mesmo Tenant.
 */
test.describe.configure({ mode: 'serial' });

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    // 1. Navega para o dashboard do motorista
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // 2. Verifica se já existe uma entrega ativa (Resiliência a falhas de cleanup)
    const activeView = page.getByTestId('driver.delivery.active');
    if (await activeView.isVisible()) {
        console.log("⚠️ Entrega ativa detectada. Pulando fase de pickup.");
    } else {
        // 3. Localiza o card de pedido disponível
        const card = page.getByTestId('driver.delivery.order.card').first();
        await expect(card).toBeVisible({ 
            timeout: 15000,
            message: "ERRO: Nenhum pedido disponível. Execute 'python scripts/maintenance/seed_ui_states.py' antes do teste."
        });
        
        // 4. Prepara a captura da resposta de rede
        const dispatchPromise = page.waitForResponse(resp => 
            resp.url().includes('/dispatch') && resp.status() === 200
        );

        // 5. Executa o pickup
        await card.getByTestId('driver.delivery.order.pickup').click({ force: true });
        await dispatchPromise;
    }

    // 6. Valida transição para modo navegação ativa
    await expect(page.getByTestId('driver.delivery.active')).toBeVisible({ timeout: 15000 });
});

test('Test 10: Client Passive Tracking', async ({ page }) => {
    // 1. Obtém um pedido para rastreio
    await page.goto('/admin/hamburgueria-ze/driver');
    
    const availableCard = page.getByTestId('driver.delivery.order.card').first();
    const activeCard = page.getByTestId('driver.delivery.active');

    let orderId: string | null = null;

    if (await activeCard.isVisible()) {
        orderId = await activeCard.getAttribute('data-order-id');
    } else if (await availableCard.isVisible()) {
        orderId = await availableCard.getAttribute('data-order-id');
    }

    if (!orderId) {
        throw new Error("Abortando: Nenhum pedido encontrado para teste de rastreamento.");
    }

    // 2. Navega para a visão do cliente
    await page.goto(`/hamburgueria-ze/menu?order=${orderId}`);
    
    // 3. Valida renderização da UI de status
    await expect(page.locator('h1')).toContainText('Olá', { timeout: 15000 });
    await expect(page.getByTestId('customer.order.stepper')).toBeVisible();
});
