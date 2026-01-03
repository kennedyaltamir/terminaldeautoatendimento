import { test, expect } from '@playwright/test';

const API_URL = 'http://127.0.0.1:8000';

test('Botão de Impressão Nativa (RawBT) deve gerar link correto', async ({ page, request }) => {
  // 1. Mock do window.location
  await page.addInitScript(() => {
    Object.defineProperty(window, 'location', {
      value: { href: '' },
      writable: true
    });
  });

  console.log('🧹 Setup: Preparando ambiente...');

  // 2. Autenticação
  const authRes = await request.post(`${API_URL}/api/auth/token`, {
    form: { username: 'admin@mesaflow.com', password: '123456' }
  });
  expect(authRes.ok(), 'Falha no login de setup').toBeTruthy();
  const { access_token } = await authRes.json();
  const headers = { Authorization: `Bearer ${access_token}` };

  // 3. Garantir que a Mesa 1 está aberta (Regra de Negócio)
  // Primeiro fechamos para garantir estado limpo
  await request.post(`${API_URL}/api/admin/tables/1/close`, {
    headers,
    data: { payment_method: 'cash' }
  });
  
  // Agora abrimos
  const openRes = await request.post(`${API_URL}/api/admin/tables/1/open`, {
    headers,
    data: { customer_name: "Print Bot" }
  });
  expect(openRes.ok(), 'Falha ao abrir mesa').toBeTruthy();

  // 4. Buscar produto
  const menuRes = await request.get(`${API_URL}/api/hamburgueria-ze/menu`);
  const menuData = await menuRes.json();
  const product = menuData.categories[0]?.products[0];

  // 5. Criar pedido na mesa aberta
  const orderPayload = {
    table_id: 1,
    qr_token: "staff-override",
    customer_name: "Print Bot",
    payment_method: "cash",
    items: [{ product_id: product.id, quantity: 1 }]
  };

  const orderRes = await request.post(`${API_URL}/api/hamburgueria-ze/orders`, {
    data: orderPayload
  });
  expect(orderRes.ok(), 'Falha ao criar pedido').toBeTruthy();

  // 6. Acessar KDS
  await page.goto('/admin/login', { waitUntil: 'domcontentloaded' });
  await page.fill('input[name="email"]', 'admin@mesaflow.com');
  await page.fill('input[name="password"]', '123456');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');
  
  await page.goto('/admin/hamburgueria-ze/kitchen', { waitUntil: 'domcontentloaded' });
  
  // 7. Testar Botão
  // Espera o card aparecer (pode demorar o polling/websocket)
  const orderCard = page.locator('div', { hasText: 'Print Bot' }).first();
  await expect(orderCard).toBeVisible({ timeout: 20000 });

  const printBtn = orderCard.locator('button[title="Imprimir (RawBT)"]');
  await expect(printBtn).toBeVisible();
  await printBtn.click();
  
  // 8. Validar
  const href = await page.evaluate(() => window.location.href);
  console.log('🖨️ URL Gerada:', href.substring(0, 50) + '...');
  expect(href).toContain('rawbt:base64,');
});