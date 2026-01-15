import { test, expect } from '@playwright/test';

/**
 * ARCHITECTURAL NOTE:
 * Este teste valida apenas contratos de estado persistente (Success Path).
 * Feedbacks visuais efêmeros (toasts) são intencionalmente ignorados para evitar flakiness em CI.
 * REQUISITO: O banco deve conter o pedido 'Cliente Happy Path' no estado 'READY'.
 */

test.describe('Logistics E2E: Happy Path', () => {
  test('Fluxo Completo: Coleta -> Entrega -> Conclusão', async ({ page }) => {
    // 1. Login Admin/Driver
    await page.goto('/admin/login');
    await page.fill('input[name="email"]', 'admin@mesaflow.com');
    await page.fill('input[name="password"]', '123456');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard');

    // 2. Acessar Painel do Motorista
    await page.goto('/admin/hamburgueria-ze/driver');

    // 3. Localizar Pedido "Cliente Happy Path" (Criado pelo Seed)
    const customerName = "Cliente Happy Path";
    
    // Verifica se a mensagem de "Vazio" está na tela (Indica falta de SEED)
    const emptyState = page.getByText('Nenhum pedido pronto para coleta');
    if (await emptyState.isVisible()) {
        throw new Error("❌ TEST DATA MISSING: O painel está vazio. Execute 'python scripts/maintenance/seed_logistics.py' antes de rodar este teste.");
    }

    const orderCard = page.getByTestId('driver.delivery.order.card').filter({ hasText: customerName }).first();
    
    // Valida visibilidade do card
    await expect(orderCard, `Pedido '${customerName}' não encontrado. Verifique o Seed.`).toBeVisible({ timeout: 15000 });

    // 4. Pegar Pedido (Dispatch)
    page.on('dialog', dialog => dialog.accept());
    const pickupBtn = orderCard.getByTestId('driver.delivery.order.pickup');
    
    const dispatchPromise = page.waitForResponse(resp => 
      resp.url().includes('/dispatch') && (resp.status() === 200 || resp.status() === 201)
    );
    await pickupBtn.click();
    await dispatchPromise;

    // 5. Validar Transição para "Em Rota"
    await expect(pickupBtn).not.toBeVisible({ timeout: 10000 });
    
    const activePanel = page.getByTestId('driver.delivery.active');
    await expect(activePanel).toBeVisible({ timeout: 15000 });
    await expect(activePanel).toContainText(customerName);

    // 6. Finalizar Entrega
    const finishBtn = page.locator('button').filter({ hasText: 'Finalizar Entrega' }).first();
    await expect(finishBtn).toBeVisible({ timeout: 10000 });

    const completePromise = page.waitForResponse(resp => 
        resp.url().includes('/complete') && resp.status() === 200
    );

    await finishBtn.click();
    await completePromise;

    // 7. Validar Sucesso (Desmontagem do Painel de Entrega Ativa)
    await expect(activePanel).not.toBeVisible({ timeout: 15000 });
  });
});
