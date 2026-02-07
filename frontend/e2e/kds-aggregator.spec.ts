import { test, expect } from '@playwright/test';

test.describe('KDS Item Aggregator', () => {
  test('deve agrupar itens iguais de pedidos diferentes', async ({ page, context }) => {
    // 1. Injetar Token
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'kitchen');
    });

    // 2. Mock Auth
    await page.route('**/api/admin/company/me', async (route) => {
      await route.fulfill({ 
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ name: "Hamburgueria Zé", plan_tier: "pro", owner_email: "admin@teste.com" })
      });
    });

    // 3. Mock Pedidos
    await page.route('**/api/admin/hamburgueria-ze/orders', async (route) => {
      const mockOrders = [
        {
          id: 'order-1',
          status: 'pending',
          items: [{ product: { id: 1, name: 'X-Bacon', station: 'kitchen' }, quantity: 2, selected_options: [] }]
        },
        {
          id: 'order-2',
          status: 'preparing',
          items: [{ product: { id: 1, name: 'X-Bacon', station: 'kitchen' }, quantity: 3, selected_options: [] }]
        }
      ];
      await route.fulfill({ json: mockOrders });
    });

    await page.route('**/api/admin/hamburgueria-ze/service-requests', async (route) => {
      await route.fulfill({ json: [] });
    });

    // 4. Navegar
    await page.goto('/admin/hamburgueria-ze/kitchen');
    await expect(page).toHaveURL(/\/kitchen/);

    // 5. Abrir Agrupador
    const aggregatorBtn = page.locator('button[title="Resumo de Produção"]');
    await expect(aggregatorBtn).toBeVisible({ timeout: 10000 });
    await aggregatorBtn.click();

    // 6. Verificar conteúdo
    // CORREÇÃO: Seletor específico para o painel lateral (classe .fixed.right-0)
    // Isso evita pegar os divs pais (layout) que também contêm o texto
    const panel = page.locator('.fixed.right-0').filter({ hasText: 'Total acumulado na fila' });
    await expect(panel).toBeVisible();

    // Busca "5" e "X-Bacon" APENAS dentro do painel
    await expect(panel.getByText('5', { exact: true })).toBeVisible();
    
    // Busca o título do item dentro do painel (h3)
    await expect(panel.locator('h3', { hasText: 'X-Bacon' })).toBeVisible();
  });
});
