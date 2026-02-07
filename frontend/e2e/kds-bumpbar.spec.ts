import { test, expect } from '@playwright/test';

test.describe('KDS Bump Bar Shortcuts', () => {
  test('deve avançar status do pedido ao pressionar tecla numerica', async ({ page, context }) => {
    // 1. Setup Auth
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'kitchen');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });

    // 2. Mocks
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Cozinha Zé", plan_tier: "pro" } });
    });

    // Mock Pedido Pendente
    await page.route('**/api/admin/hamburgueria-ze/orders', async route => {
      await route.fulfill({ 
        status: 200, 
        json: [
          { 
            id: 'ord-shortcut', 
            status: 'pending', 
            customer_name: 'Mesa 5', 
            created_at: new Date().toISOString(),
            items: [{ id: 99, product: { id: 1, name: 'Fritas', station: 'kitchen' }, quantity: 1 }] 
          }
        ] 
      });
    });

    // Interceptar a chamada de atualização de status
    let statusUpdated = false;
    await page.route('**/api/admin/orders/ord-shortcut', async route => {
        if (route.request().method() === 'PATCH') {
            const data = JSON.parse(route.request().postData() || '{}');
            if (data.status === 'preparing') statusUpdated = true;
            await route.fulfill({ status: 200, json: { message: "OK" } });
        }
    });

    await page.route('**/api/admin/hamburgueria-ze/service-requests', async route => {
      await route.fulfill({ json: [] });
    });

    // 3. Navegar
    await page.goto('/admin/hamburgueria-ze/kitchen');

    // 4. Aguardar renderização do card antes de pressionar a tecla
    // Isso garante que o componente React montou os event listeners
    await expect(page.locator('text=Mesa 5')).toBeVisible({ timeout: 15000 });
    
    // Pequena pausa para estabilização de hidratação
    await page.waitForTimeout(1000);

    // 5. Pressionar tecla '1'
    await page.keyboard.press('1');

    // 6. Verificar se a API foi chamada via Polling
    await expect.poll(() => statusUpdated, {
        timeout: 10000,
        message: "O atalho de teclado '1' não disparou a atualização de status."
    }).toBe(true);
  });
});
