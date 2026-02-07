import { test, expect } from '@playwright/test';

test.describe('Sticker Printing', () => {
  test('deve gerar código ZPL ao clicar no botão de etiqueta', async ({ page, context }) => {
    // 1. Mock do window.location (Estratégia de Interceptação de Protótipo)
    await page.addInitScript(() => {
      (window as any).__intentUrl = '';
      // Sobrescreve o setter de href no protótipo para capturar a atribuição
      const originalDescriptor = Object.getOwnPropertyDescriptor(window.Location.prototype, 'href');
      Object.defineProperty(window.Location.prototype, 'href', {
        set: function(value) {
          console.log('Playwright Intercepted Navigation:', value);
          (window as any).__intentUrl = value;
        },
        get: function() {
          return originalDescriptor?.get?.call(this) || '';
        },
        configurable: true
      });
    });

    // 2. Mock do User Agent para simular Android (Gatilho do RawBT)
    await context.addInitScript(() => {
      Object.defineProperty(navigator, 'userAgent', {
        value: 'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36',
        configurable: true
      });
    });

    // 3. Setup Auth
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'kitchen');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });

    // 4. Mocks de API
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Cozinha Zé", plan_tier: "pro" } });
    });

    await page.route('**/api/admin/hamburgueria-ze/orders', async route => {
      await route.fulfill({ 
        status: 200, 
        json: [
          { 
            id: 'ord-sticker-test', 
            status: 'preparing', 
            customer_name: 'Mesa 10', 
            created_at: new Date().toISOString(),
            order_type: 'dine_in',
            total_amount: 20.00,
            payment_status: 'paid',
            payment_method: 'cash',
            table: { table_number: 10 },
            items: [{ 
                id: 101, 
                product: { id: 1, name: 'Burger', station: 'kitchen', price: 20.00 }, 
                quantity: 1, 
                selected_options: [] 
            }] 
          }
        ] 
      });
    });

    await page.route('**/api/admin/hamburgueria-ze/service-requests', async route => {
      await route.fulfill({ json: [] });
    });

    // 5. Navegar
    await page.goto('/admin/hamburgueria-ze/kitchen');

    // 6. Clicar no botão de etiqueta
    const tagBtn = page.locator('button[title="Imprimir Etiqueta"]');
    await expect(tagBtn).toBeVisible({ timeout: 15000 });
    await tagBtn.click({ force: true });

    // 7. Verificar Intent via Polling
    await expect.poll(async () => {
        return await page.evaluate(() => (window as any).__intentUrl);
    }, { 
        timeout: 10000,
        message: "O link de impressão RawBT não foi gerado."
    }).toContain('rawbt:base64,');
    
    const intentUrl = await page.evaluate(() => (window as any).__intentUrl);
    const base64 = intentUrl.split(',')[1];
    const decoded = Buffer.from(base64, 'base64').toString('utf-8');
    
    expect(decoded).toContain('^XA');
    expect(decoded).toContain('Burger');
  });
});
