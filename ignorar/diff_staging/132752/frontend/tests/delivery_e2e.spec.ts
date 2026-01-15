import { test, expect } from '@playwright/test';

test.describe('Logistics E2E: Happy Path', () => {
  test('Fluxo Completo: Coleta -> Entrega -> Conclusão', async ({ page }) => {
    // Monitorar erros de console e rede para debug
    page.on('console', msg => console.log(`CONSOLE: ${msg.text()}`));
    page.on('response', response => {
      if (response.status() >= 400) {
        console.log(`HTTP ERROR: ${response.url()} ${response.status()}`);
      }
    });

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
    
    // Valida que está na lista "A Retirar" (Disponíveis)
    await expect(orderCard, `Pedido '${customerName}' não encontrado na lista.`).toBeVisible({ timeout: 10000 });

    // 4. Pegar Pedido (Dispatch)
    page.on('dialog', dialog => dialog.accept());
    const pickupBtn = orderCard.getByTestId('driver.delivery.order.pickup');
    
    // Captura a requisição de dispatch para garantir que foi enviada e aceita
    const dispatchPromise = page.waitForResponse(resp => 
      resp.url().includes('/dispatch') && (resp.status() === 200 || resp.status() === 201)
    );
    await pickupBtn.click();
    await dispatchPromise;

    // 5. Validar Transição para "Em Rota"
    // Espera o botão sumir (estado local atualizado)
    await expect(pickupBtn).not.toBeVisible({ timeout: 10000 });
    
    // Agora validamos o painel ativo
    const activePanel = page.getByTestId('driver.delivery.active');
    await expect(activePanel).toBeVisible({ timeout: 15000 });
    await expect(activePanel).toContainText(customerName);

    // 6. Finalizar Entrega
    const finishBtn = page.locator('button').filter({ hasText: 'Finalizar Entrega' }).first();
    await expect(finishBtn).toBeVisible({ timeout: 10000 });

    // 🛡️ ROBUSTNESS FIX: Wait for the network response of the completion action
    // This guarantees that the backend has processed the request before we check for UI changes.
    const completePromise = page.waitForResponse(resp => 
        resp.url().includes('/complete') && resp.status() === 200
    );

    await finishBtn.click();
    
    // Wait for the backend to confirm success
    await completePromise;

    // 7. Validar Sucesso (Estratégia Paralela)
    // Agora que sabemos que o backend respondeu 200, o toast DEVE aparecer.
    await Promise.all([
        expect(page.getByText('Entrega finalizada!')).toBeVisible({ timeout: 5000 }),
        expect(activePanel).not.toBeVisible({ timeout: 15000 })
    ]);
  });
});
