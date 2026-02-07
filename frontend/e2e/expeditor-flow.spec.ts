import { test, expect } from '@playwright/test';

test.describe('Expeditor Flow', () => {
  test('deve listar pedidos prontos e permitir despacho', async ({ page, context }) => {
    // 1. Setup Auth
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'kitchen');
    });

    // 2. Mocks
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Cozinha Zé", plan_tier: "pro" } });
    });

    // Mock de Pedidos (1 Preparando, 1 Pronto)
    await page.route('**/api/admin/hamburgueria-ze/orders', async route => {
      await route.fulfill({ 
        status: 200, 
        json: [
          { 
            id: 'ord-prep', 
            status: 'preparing', 
            customer_name: 'Mesa 10', 
            items: [{ product: { name: 'Burger', station: 'kitchen' }, quantity: 1 }] 
          },
          { 
            id: 'ord-ready', 
            status: 'ready', 
            customer_name: 'Mesa 12', 
            created_at: new Date().toISOString(),
            items: [{ product: { name: 'Fritas', station: 'kitchen' }, quantity: 2 }] 
          }
        ] 
      });
    });

    // Mock de Despacho
    await page.route('**/api/admin/orders/ord-ready', async route => {
      const method = route.request().method();
      if (method === 'PATCH') {
        await route.fulfill({ status: 200, json: { message: "Despachado" } });
      }
    });

    // 3. Navegar
    await page.goto('/admin/hamburgueria-ze/expeditor');

    // 4. Verificar Colunas
    await expect(page.getByText('Em Produção')).toBeVisible();
    await expect(page.getByText('Pronto para Montagem')).toBeVisible();

    // 5. Verificar Pedidos
    await expect(page.getByText('Mesa 10')).toBeVisible(); // Preparando
    await expect(page.getByText('Mesa 12')).toBeVisible(); // Pronto

    // 6. Despachar
    await page.getByText('Despachar / Servir').click();

    // 7. Sucesso
    await expect(page.getByText('Pedido Mesa 12 despachado!')).toBeVisible();
  });
});
