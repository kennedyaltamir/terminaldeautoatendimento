import { test, expect } from '@playwright/test';

test.describe('Split Bill Flow', () => {
  test('deve permitir dividir a conta e pagar parcialmente', async ({ page, context }) => {
    // 1. Setup Auth
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'cashier');
    });

    // 2. Mocks
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Bar do Zé", plan_tier: "pro" } });
    });

    await page.route('**/api/hamburgueria-ze/check-table', async route => {
      await route.fulfill({ status: 200, json: { status: 'active', session_token: 'sess-123', customer_name: 'Grupo' } });
    });

    await page.route('**/api/hamburgueria-ze/session/sess-123', async route => {
      await route.fulfill({ status: 200, json: { 
        id: 123, 
        customer_name: 'Grupo', 
        total_spent: 100.00, 
        orders: [
          { id: 'ord-1', total_amount: 50.00, payment_status: 'pending', items: [{ product: { name: "Picanha", price: 50.00 }, quantity: 1, selected_options: [] }] },
          { id: 'ord-2', total_amount: 50.00, payment_status: 'pending', items: [{ product: { name: "Cerveja", price: 50.00 }, quantity: 1, selected_options: [] }] }
        ] 
      }});
    });

    await page.route('**/api/hamburgueria-ze/menu', async route => {
      await route.fulfill({ status: 200, json: { company: { name: "Bar do Zé" }, categories: [] } });
    });

    // Mock do Pagamento Parcial
    await page.route('**/api/admin/tables/1/pay', async route => {
      const data = JSON.parse(route.request().postData() || '{}');
      if (data.amount === 50) {
        await route.fulfill({ status: 200, json: { message: "Pagamento parcial OK" } });
      } else {
        await route.fulfill({ status: 400, json: { detail: "Valor incorreto" } });
      }
    });

    // 3. Navegar
    await page.goto('/admin/hamburgueria-ze/waiter/pos/1');

    // 4. Abrir Split
    await page.getByTitle('Dividir Conta').click();
    await expect(page.getByText('Dividir Igual')).toBeVisible();

    // 5. Dividir por 2 pessoas (Padrão)
    // Total 100 / 2 = 50
    await expect(page.getByText('R$ 50.00')).toBeVisible();

    // 6. Confirmar Valor
    await page.getByText('Pagar Agora').click();

    // 7. Modal de Pagamento deve abrir com valor parcial
    await expect(page.getByText('Pagamento Parcial: Mesa 1')).toBeVisible();
    await expect(page.getByText('R$ 50.00')).toBeVisible();

    // 8. Pagar
    await page.getByText('Dinheiro').click();
    await page.getByText('Pagar Parcial').click();

    // 9. Sucesso
    await expect(page.getByText('Pagamento de R$ 50.00 registrado!')).toBeVisible();
  });
});
