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
    
    // FIX: Usar o test-id do card para garantir que pegamos o container correto
    const orderCard = page.getByTestId('driver.delivery.order.card').filter({ hasText: customerName }).first();
    
    // Valida que está na lista "A Retirar" (Disponíveis)
    await expect(orderCard, `Pedido '${customerName}' não encontrado na lista.`).toBeVisible({ timeout: 10000 });
    
    // 4. Pegar Pedido (Dispatch)
    page.on('dialog', dialog => dialog.accept());

    const pickupBtn = orderCard.getByTestId('driver.delivery.order.pickup');
    
    // Captura a requisição de dispatch para garantir que foi enviada e aceita
    // Isso evita "flakiness" onde a UI demora para atualizar mas o backend já processou
    const dispatchPromise = page.waitForResponse(resp => 
      resp.url().includes('/dispatch') && resp.status() === 200
    );

    await pickupBtn.click();
    
    // Aguarda a confirmação do backend
    await dispatchPromise;
    
    // 5. Validar Transição para "Em Rota"
    // O card deve mudar de estado ou mover para a seção ativa.
    // Vamos esperar que o botão "Pegar" suma, indicando que a ação foi processada.
    await expect(pickupBtn).not.toBeVisible({ timeout: 10000 });

    // FIX: Forçar reload para garantir estado atualizado se o WS falhar no ambiente de teste
    await page.reload();

    // Agora validamos o painel ativo
    const activePanel = page.getByTestId('driver.delivery.active');
    await expect(activePanel).toBeVisible({ timeout: 15000 });
    await expect(activePanel).toContainText(customerName);
    
    // 6. Finalizar Entrega
    // O botão pode demorar um pouco para renderizar após a transição de estado
    // Usamos um seletor mais genérico para garantir
    const finishBtn = page.locator('button').filter({ hasText: 'Finalizar Entrega' }).first();
    await expect(finishBtn).toBeVisible({ timeout: 10000 });
    await finishBtn.click();
    
    // 7. Validar que voltou para o estado inicial (sem entrega ativa)
    await expect(activePanel).not.toBeVisible({ timeout: 10000 });
    
    // Opcional: Verificar toast de sucesso
    await expect(page.getByText('Entrega finalizada!')).toBeVisible();
  });
});
