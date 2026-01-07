import { test, expect } from '@playwright/test';

test.describe('Driver Cash Management', () => {
  test('deve listar motoristas com dívida e permitir baixa', async ({ page, context }) => {
    // 1. Setup Auth
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'manager');
    });

    // 2. Mocks
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Logística Zé", plan_tier: "pro" } });
    });

    // Mock da lista de pedidos (vazia para focar no modal)
    await page.route('**/api/admin/delivery/orders', async route => {
      await route.fulfill({ status: 200, json: [] });
    });

    // Mock da lista de devedores
    await page.route('**/api/admin/logistics/drivers', async route => {
      await route.fulfill({ 
        status: 200, 
        json: [
          { driver_id: 1, driver_name: "João Motoboy", current_debt: 50.00 },
          { driver_id: 2, driver_name: "Maria Driver", current_debt: 0.00 } // Não deve aparecer
        ] 
      });
    });

    // Mock da baixa
    await page.route('**/api/admin/logistics/drivers/1/settle', async route => {
      const data = JSON.parse(route.request().postData() || '{}');
      if (data.amount === 50) {
        await route.fulfill({ status: 200, json: { message: "Pago" } });
      } else {
        await route.fulfill({ status: 400 });
      }
    });

    // 3. Navegar
    await page.goto('/admin/hamburgueria-ze/delivery');

    // 4. Abrir Modal
    await page.getByText('Prestação de Contas').click();
    await expect(page.getByText('Selecione um entregador')).toBeVisible();

    // 5. Verificar Lista
    await expect(page.getByText('João Motoboy')).toBeVisible();
    await expect(page.getByText('R$ 50.00')).toBeVisible();
    await expect(page.getByText('Maria Driver')).toBeHidden(); // Saldo zero não aparece

    // 6. Selecionar Motorista
    await page.getByText('João Motoboy').click();
    await expect(page.getByText('Dívida Total:')).toBeVisible();

    // 7. Confirmar Baixa (Valor já vem preenchido)
    await page.getByText('Confirmar Baixa').click();

    // 8. Sucesso
    await expect(page.getByText('Pagamento registrado!')).toBeVisible();
  });
});
