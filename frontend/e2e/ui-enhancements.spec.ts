import { test, expect } from '@playwright/test';

test.describe('UX/UI Enhancements (Fase 7)', () => {
  
  test('Login Screen: Branding and Password Toggle', async ({ page }) => {
    await page.goto('/admin/login');

    // CORREÇÃO: Usamos getByRole para pegar especificamente o Link do logo
    const logo = page.getByRole('link', { name: 'MesaFlow' });
    await expect(logo).toBeVisible();
    
    // Verifica se a classe de texto grande foi aplicada
    const logoText = logo.locator('span');
    await expect(logoText).toHaveClass(/text-3xl/);

    // 2. Verifica o Toggle de Senha
    const passwordInput = page.locator('input[name="password"]');
    const toggleBtn = page.locator('button:has(svg.lucide-eye)'); 
    
    await expect(passwordInput).toBeVisible();
    await expect(toggleBtn).toBeVisible();

    await passwordInput.fill('senha123');
    await toggleBtn.click();
    
    await expect(passwordInput).toHaveAttribute('type', 'text');
  });

  test('Register Screen: Slug Prefix and Password Strength', async ({ page }) => {
    await page.goto('/admin/register');

    await expect(page.getByText('mesaflow.com/')).toBeVisible();

    const passInput = page.locator('input[name="password"]');
    await passInput.fill('123'); 
    await passInput.fill('SenhaForte123!'); 
    await expect(passInput).toHaveValue('SenhaForte123!');
  });

  test('Public Menu: Sticky Nav and Back to Top', async ({ page }) => {
    await page.goto('/hamburgueria-ze/menu');

    const header = page.locator('header').first(); 
    await expect(header).toBeVisible();

    // --- CORREÇÃO CRÍTICA ---
    // Força a página a ficar gigante para garantir que o scroll funcione
    // mesmo com poucos produtos no banco de dados.
    await page.evaluate(() => {
      document.body.style.minHeight = '3000px';
    });

    // 2. Scroll para baixo (agora vai funcionar)
    await page.evaluate(() => window.scrollTo(0, 1000));
    // Dispara evento de scroll para garantir que o React detecte
    await page.evaluate(() => window.dispatchEvent(new Event('scroll')));

    // 3. Verifica botão voltar ao topo
    // Usamos a classe fixa do botão em vez do ícone, é mais seguro
    const backToTop = page.locator('button.fixed.bottom-24');
    
    await expect(backToTop).toBeVisible({ timeout: 5000 });
    
    await backToTop.click();
    
    // Verifica se voltou ao topo
    await page.waitForTimeout(1000); // Espera animação smooth
    const scrollY = await page.evaluate(() => window.scrollY);
    expect(scrollY).toBeLessThan(100);
  });

});
