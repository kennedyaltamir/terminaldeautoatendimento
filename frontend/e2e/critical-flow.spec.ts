import { test, expect } from '@playwright/test';

const API_URL = 'http://127.0.0.1:8000';

test('Fluxo Crítico: Pedido do Cliente reflete no KDS em Tempo Real', async ({ browser, request }) => {
  
  // --- SETUP ---
  console.log('🧹 Setup: Resetando mesa...');
  const authRes = await request.post(`${API_URL}/api/auth/token`, {
    form: { username: 'admin@mesaflow.com', password: '123456' }
  });
  expect(authRes.ok()).toBeTruthy();
  const { access_token } = await authRes.json();

  // Resetar mesa 1
  await request.post(`${API_URL}/api/admin/tables/1/close`, {
    headers: { Authorization: `Bearer ${access_token}` },
    data: { payment_method: 'cash' }
  });

  // --- NAVEGADORES ---
  const adminContext = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const adminPage = await adminContext.newPage();

  const customerContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    isMobile: true,
    hasTouch: true
  });
  const customerPage = await customerContext.newPage();

  // --- 1. ADMIN ABRE KDS ---
  await adminPage.goto('/admin/login');
  await adminPage.fill('input[name="email"]', 'admin@mesaflow.com');
  await adminPage.fill('input[name="password"]', '123456');
  await adminPage.click('button[type="submit"]');
  await adminPage.waitForURL('**/dashboard');
  await adminPage.goto('/admin/hamburgueria-ze/kitchen');
  await expect(adminPage.getByText('Monitor de Produção')).toBeVisible();

  // --- 2. CLIENTE FAZ PEDIDO ---
  await customerPage.goto('/hamburgueria-ze/menu?mesa=1&token=token-seguro-mesa-1');
  
  // Check-in OBRIGATÓRIO (Pois resetamos a mesa)
  const nameInput = customerPage.getByPlaceholder('Seu Nome');
  await expect(nameInput).toBeVisible({ timeout: 10000 }); // Espera explícita
  await nameInput.fill('Robô E2E');
  await customerPage.getByRole('button', { name: /Abrir/i }).click();

  // Esperar menu carregar
  await expect(customerPage.getByText('Lanches')).toBeVisible({ timeout: 10000 });

  // Adicionar Produto
  const productCard = customerPage.locator('div', { hasText: 'X-Bacon' }).first();
  await productCard.click();

  // Modal
  const addBtn = customerPage.getByRole('button', { name: /Adicionar/i });
  await expect(addBtn).toBeVisible();
  await addBtn.click();
  await expect(addBtn).toBeHidden();

  // Carrinho
  const cartBtn = customerPage.getByRole('button', { name: /Ver Carrinho/i });
  await expect(cartBtn).toBeVisible();
  await cartBtn.click();

  // Enviar
  await customerPage.click('text=DINHEIRO');
  await customerPage.click('button:has-text("Enviar Pedido")');

  // Sucesso
  await expect(customerPage.getByText('Pedido enviado!')).toBeVisible({ timeout: 15000 });

  // --- 3. VERIFICAR NO KDS ---
  const kdsCard = adminPage.locator('div', { hasText: 'Robô E2E' });
  await expect(kdsCard).toBeVisible({ timeout: 15000 });
  await expect(kdsCard).toContainText('X-Bacon');
  
  console.log('✅ Fluxo E2E concluído com sucesso!');
});