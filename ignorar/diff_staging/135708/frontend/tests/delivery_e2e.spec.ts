import { test, expect } from '@playwright/test';

test.describe('Logistics E2E: Happy Path', () => {
  test('Fluxo Completo: Coleta -> Entrega -> Conclusão', async ({ page }) => {
    test.setTimeout(60000);
    
    // 1. Login Admin
    await page.goto('/admin/login');
    await page.fill('input[name="email"]', 'admin@mesaflow.com');
    await page.fill('input[name="password"]', '123456');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard');

    // 2. Acessar Painel do Motorista
    await page.goto('/admin/hamburgueria-ze/driver');
    await page.waitForLoadState('networkidle');

    // 3. Localizar Pedido Disponível (Criado pelo Seed)
    const orderCard = page.getByTestId('driver.delivery.order.card').first();
    await expect(orderCard, "ERRO: Nenhum pedido disponível para coleta. Verifique o Seed.").toBeVisible({ timeout: 15000 });
    const customerName = await orderCard.locator('h3').textContent();

    // 4. Pegar Pedido (Dispatch)
    page.on('dialog', dialog => dialog.accept());
    
    const dispatchPromise = page.waitForResponse(resp => 
      resp.url().includes('/dispatch') && (resp.status() === 200 || resp.status() === 201)
    );
    
    await orderCard.getByTestId('driver.delivery.order.pickup').click();
    await dispatchPromise;

    // 5. Validar Transição para Painel Ativo
    const activePanel = page.getByTestId('driver.delivery.active');
    await expect(activePanel).toBeVisible({ timeout: 15000 });
    if (customerName) {
      await expect(activePanel).toContainText(customerName);
    }

    // 6. Finalizar Entrega
    const finishBtn = page.locator('button').filter({ hasText: 'Finalizar Entrega' }).first();
    await expect(finishBtn).toBeVisible({ timeout: 10000 });
    
    const completePromise = page.waitForResponse(resp => 
        resp.url().includes('/complete') && (resp.status() === 200 || resp.status() === 201)
    );

    await finishBtn.click();
    await completePromise;

    // 7. Validar Retorno ao Estado Inicial (Sem entrega ativa)
    await expect(activePanel).not.toBeVisible({ timeout: 15000 });
    await expect(page.getByText('Entrega finalizada!')).toBeVisible();
  });
});
