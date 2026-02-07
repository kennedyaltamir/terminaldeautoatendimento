import { test, expect } from '@playwright/test';

test.describe('Counter POS (Balcão)', () => {
  test('Should load Counter interface and add items', async ({ page }) => {
    // Login como Admin
    await page.goto('/admin/login');
    await page.fill('input[name="email"]', 'admin@mesaflow.com');
    await page.fill('input[name="password"]', '123456');
    await page.click('button[type="submit"]');
    
    // Navegar para Balcão
    await page.goto('/admin/hamburgueria-ze/counter');
    
    // Verificar colunas
    await expect(page.getByText('Carrinho Atual')).toBeVisible();
    await expect(page.getByText('Em Produção')).toBeVisible();

    // Adicionar item (X-Bacon do seed)
    // Procura um botão que contenha o texto X-Bacon
    const productBtn = page.locator('button').filter({ hasText: 'X-Bacon' }).first();
    await expect(productBtn).toBeVisible();
    await productBtn.click();

    // Verificar se foi pro carrinho
    await expect(page.locator('text=1x X-Bacon')).toBeVisible();
    
    // Verificar total
    await expect(page.locator('text=R$ 28.90')).toBeVisible();
  });
});
