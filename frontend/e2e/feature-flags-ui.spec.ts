import { test, expect } from '@playwright/test';

/**
 * Testes E2E para a UI de Feature Flags.
 * Valida renderização, segurança de impersonation e feedback de erro.
 */

test.describe('Feature Flags UI & UX', () => {
  const SLUG = 'hamburgueria-ze';
  const FEATURES_URL = `/admin/${SLUG}/settings/features`;

  test('deve exibir tela de acesso negado para usuários comuns', async ({ page }) => {
    // 1. Simular Token de Dono Comum (impersonator: false)
    const fakeToken = "header." + btoa(JSON.stringify({ sub: "owner@test.com", impersonator: false })) + ".signature";
    
    await page.addInitScript((token) => {
      window.localStorage.setItem('mesaflow_access_token', token);
      window.localStorage.setItem('mesaflow_user_role', 'owner');
    }, fakeToken);

    await page.goto(FEATURES_URL);

    // 2. Validar se a mensagem de restrição aparece
    await expect(page.getByText('Acesso Restrito')).toBeVisible();
    await expect(page.locator('button[aria-label*="Alternar"]')).not.toBeVisible();
  });

  test('deve listar flags e permitir toggle em modo suporte', async ({ page }) => {
    // 1. Simular Token de Suporte (impersonator: true)
    const fakeToken = "header." + btoa(JSON.stringify({ sub: "support@mesaflow.com", impersonator: true })) + ".signature";
    
    await page.addInitScript((token) => {
      window.localStorage.setItem('mesaflow_access_token', token);
      window.localStorage.setItem('mesaflow_user_role', 'owner');
    }, fakeToken);

    // 2. Mock da API
    await page.route('**/api/admin/features', async route => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ 
          status: 200, 
          body: JSON.stringify({ "beta_feature_test": false }) 
        });
      } else if (route.request().method() === 'POST') {
        await route.fulfill({ 
          status: 200, 
          body: JSON.stringify({ "status": true }) 
        });
      }
    });

    await page.goto(FEATURES_URL);

    // 3. Validar renderização
    await expect(page.getByText('Modo Suporte Ativo')).toBeVisible();
    const toggle = page.locator('button[aria-label*="Alternar"]');
    await expect(toggle).toBeVisible();

    // 4. Executar Toggle
    await toggle.click();

    // 5. Verificar Toast de sucesso (Sonner)
    await expect(page.getByText('Funcionalidade ativada com sucesso')).toBeVisible();
  });

  test('deve reverter estado visual em caso de erro 422 (Fail Secure)', async ({ page }) => {
    const fakeToken = "header." + btoa(JSON.stringify({ impersonator: true })) + ".signature";
    await page.addInitScript((token) => {
      window.localStorage.setItem('mesaflow_access_token', token);
    }, fakeToken);

    // Mock: GET retorna false, POST retorna erro
    await page.route('**/api/admin/features', async route => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ status: 200, body: JSON.stringify({ "buggy_feature": false }) });
      } else {
        await route.fulfill({ status: 422, body: JSON.stringify({ detail: "Invalid Schema" }) });
      }
    });

    await page.goto(FEATURES_URL);
    const toggle = page.locator('button[aria-label*="Alternar"]');

    // Clica para ativar
    await toggle.click();

    // Verifica se o Toast de erro apareceu
    await expect(page.getByText('Erro de validação no servidor')).toBeVisible();

    // Verifica se o botão voltou para o estado desativado (bg-gray-700)
    await expect(toggle).toHaveClass(/bg-gray-700/);
  });
});
