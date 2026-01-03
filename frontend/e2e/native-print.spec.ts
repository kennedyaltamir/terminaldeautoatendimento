import { test, expect } from '@playwright/test';

// Forçando IPv4
const API_URL = 'http://127.0.0.1:8000';

test('Botão de Impressão Nativa (RawBT) deve gerar link correto', async ({ page, request }) => {
  // 1. Mock do window.location
  await page.addInitScript(() => {
    Object.defineProperty(window, 'location', {
      value: { href: '' },
      writable: true
    });
  });

  console.log('🧹 Setup: Preparando dados para impressão...');

  // 2. Autenticação
  const authRes = await request.post(`${API_URL}/api/auth/token`, {
    form: { username: 'admin@mesaflow.com', password: '123456' }
  });
  expect(authRes.ok(), 'Falha no login de setup').toBeTruthy();
  const { access_token } = await authRes.json();
  
  // 3. Buscar produto
  const menuRes = await request.get(`${API_URL}/api/hamburgueria-ze/menu`);
  expect(menuRes.ok(), 'Falha ao buscar menu').toBeTruthy();
  const menuData = await menuRes.json();
  const product = menuData.categories[0]?.products[0];
  expect(product, 'Nenhum produto encontrado').toBeDefined();

  // 4. Criar pedido (Usando staff-override para ignorar mesa fechada)
  const orderPayload = {
    table_id: 1,
    qr_token: "staff-override", // <--- CORREÇÃO: Token mestre para criar sem sessão
    customer_name: "Print Test Bot",
    payment_method: "cash",
    items: [{ product_id: product.id, quantity: 1 }]
  };

  const orderRes = await request.post(`${API_URL}/api/hamburgueria-ze/orders`, {
    data: orderPayload
  });

  if (!orderRes.ok()) {
    console.error('❌ Erro ao criar pedido:', await orderRes.text());
  }
  expect(orderRes.ok(), 'Falha ao criar pedido de teste').toBeTruthy();

  // 5. Acessar KDS
  await page.goto('/admin/login');
  await page.fill('input[name="email"]', 'admin@mesaflow.com');
  await page.fill('input[name="password"]', '123456');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');
  
  await page.goto('/admin/hamburgueria-ze/kitchen');
  
  // 6. Testar Botão
  const orderCard = page.locator('div', { hasText: 'Print Test Bot' }).first();
  await expect(orderCard).toBeVisible({ timeout: 15000 });

  const printBtn = orderCard.locator('button[title="Imprimir (RawBT)"]');
  await expect(printBtn).toBeVisible();
  await printBtn.click();
  
  // 7. Validar
  const href = await page.evaluate(() => window.location.href);
  console.log('🖨️ URL Gerada:', href.substring(0, 50) + '...');
  expect(href).toContain('rawbt:base64,');
});