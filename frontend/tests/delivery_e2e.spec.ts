// DOMAIN: FRONTEND
import { test, expect } from '@playwright/test';

test.describe('Logistics E2E: Happy Path', () => {
  test('Fluxo Completo: Coleta -> Entrega -> Conclusão', async ({ page }) => {
    // 1. Login
    await page.goto('/admin/login');
    await page.fill('input[name="email"]', 'admin@mesaflow.com');
    await page.fill('input[name="password"]', '123456');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard');

    // 2. Acessar Painel do Motorista
    await page.goto('/admin/hamburgueria-ze/driver');
    await page.waitForLoadState('networkidle');

    // 3. Localizar Pedido (Resiliente)
    const card = page.getByTestId('driver.delivery.order.card').first();
    await expect(card, "ERRO: Nenhum pedido disponível. Execute o seed.").toBeVisible({ timeout: 20000 });

    const customerName = await card.locator('h3').textContent();
    console.log(`📦 Iniciando entrega para: ${customerName}`);

    // 4. Pegar Pedido
    page.on('dialog', d => d.accept());
    const pickupBtn = card.getByTestId('driver.delivery.order.pickup');
    
    const dispatchPromise = page.waitForResponse(r => r.url().includes('/dispatch') && r.status() === 200);
    await pickupBtn.click();
    await dispatchPromise;

    // 5. Validar Transição para Mapa
    const activePanel = page.getByTestId('driver.delivery.active');
    await expect(activePanel).toBeVisible({ timeout: 15000 });

    // 6. Finalizar Entrega
    const finishBtn = page.locator('button').filter({ hasText: 'Finalizar Entrega' }).first();
    const completePromise = page.waitForResponse(r => r.url().includes('/complete') && r.status() === 200);
    await finishBtn.click();
    await completePromise;

    // 7. Validar Sucesso
    await expect(activePanel).not.toBeVisible({ timeout: 10000 });
    console.log("✅ Fluxo validado com sucesso.");
  });
});

