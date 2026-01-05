import { test, expect } from '@playwright/test';

test('Deve exibir o modal de "Em Breve" ao clicar no botão do Google', async ({ page }) => {
  // 1. Acessar página de login
  await page.goto('/admin/login');

  // 2. Clicar no botão do Google
  const googleBtn = page.getByRole('button', { name: /Entrar com Google/i });
  await googleBtn.click();

  // 3. Verificar se o modal apareceu
  const modal = page.getByText('Funcionalidade em Homologação');
  await expect(modal).toBeVisible();

  // 4. Fechar o modal
  const closeBtn = page.getByRole('button', { name: /Entendi, obrigado!/i });
  await closeBtn.click();

  // 5. Verificar se o modal sumiu
  await expect(modal).toBeHidden();
});