import { test, expect } from '@playwright/test';

const API_URL = 'http://127.0.0.1:8000';

test('Dashboard de Franquia deve carregar e exibir dados', async ({ page, request }) => {
  // 1. Setup: Login como Admin (Dono)
  const authRes = await request.post(`${API_URL}/api/auth/token`, {
    form: { username: 'admin@mesaflow.com', password: '123456' }
  });
  expect(authRes.ok()).toBeTruthy();
  
  // 2. Acessar Login (Com espera explícita de carregamento)
  await page.goto('/admin/login', { waitUntil: 'domcontentloaded' });
  
  // Garantir que o input está visível antes de digitar
  await expect(page.locator('input[name="email"]')).toBeVisible({ timeout: 20000 });
  
  await page.fill('input[name="email"]', 'admin@mesaflow.com');
  await page.fill('input[name="password"]', '123456');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');

  // 3. Navegar para Franquia
  await page.goto('/admin/franchise', { waitUntil: 'domcontentloaded' });

  // 4. Validar Elementos
  await expect(page.getByText('Visão Multi-loja')).toBeVisible({ timeout: 20000 });
  await expect(page.getByText('Faturamento Global')).toBeVisible();
  
  // Verificar se a tabela de lojas aparece
  await expect(page.getByText('Hamburgueria do Zé')).toBeVisible();
  
  // Verificar se o botão de acesso individual existe
  const accessBtn = page.getByRole('link', { name: /Acessar/i }).first();
  await expect(accessBtn).toBeVisible();
});