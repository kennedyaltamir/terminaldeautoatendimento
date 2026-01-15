import { test, expect } from '@playwright/test';

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
    
    // FIX: Usar o test-id do card para garantir que pegamos o container correto
    const orderCard = page.getByTestId('driver.delivery.order.card').filter({ hasText: customerName }).first();
    
    // Valida que está na lista "A Retirar" (Disponíveis)
    await expect(orderCard, `Pedido '${customerName}' não encontrado na lista.`).toBeVisible({ timeout: 10000 });
    
    // 4. Pegar Pedido (Dispatch)
    page.on('dialog', dialog => dialog.accept());

    const pickupBtn = orderCard.getByTestId('driver.delivery.order.pickup');
    await pickupBtn.click();
    
    // 5. Validar Transição para "Em Rota"
    const activePanel = page.getByTestId('driver.delivery.active');
    await expect(activePanel).toBeVisible({ timeout: 15000 }); // Aumentado timeout para transição
    await expect(activePanel).toContainText(customerName);
    
    // 6. Finalizar Entrega
    // FIX: Aumentado timeout e usado seletor mais específico se possível, ou apenas aguardar
    const finishBtn = page.getByRole('button', { name: /Finalizar Entrega/i });
    await expect(finishBtn).toBeVisible({ timeout: 10000 });
    await finishBtn.click();
    
    // 7. Validar que voltou para o estado inicial (sem entrega ativa)
    await expect(activePanel).not.toBeVisible({ timeout: 10000 });
    
    // Opcional: Verificar toast de sucesso
    await expect(page.getByText('Entrega finalizada!')).toBeVisible();
  });
});
