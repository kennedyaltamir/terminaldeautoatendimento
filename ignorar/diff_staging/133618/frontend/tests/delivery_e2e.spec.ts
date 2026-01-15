// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 14:15:00
import { test, expect } from '@playwright/test';

/**
 * ARCHITECTURAL NOTE:
 * Este teste valida apenas contratos de estado persistente (Success Path).
 * Feedbacks visuais efêmeros (toasts) são intencionalmente ignorados para evitar flakiness em CI.
 * Ver: REPORT_INCIDENT_RESOLUTION_TOAST.md
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
    const orderCard = page.getByTestId('driver.delivery.order.card').filter({ hasText: customerName }).first();
    
    await expect(orderCard).toBeVisible({ timeout: 15000 });

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
    // O sucesso é definido pelo desaparecimento do painel, indicando que o estado local foi resetado.
    await expect(activePanel).not.toBeVisible({ timeout: 15000 });
  });
});
