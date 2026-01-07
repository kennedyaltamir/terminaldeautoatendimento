// Validated via atualizar.py pipeline
import { test, expect } from '@playwright/test';

const BASE_URL = 'http://127.0.0.1:3000';
const SLUG = 'hamburgueria-ze';

test.describe('Feature Flags - God Mode (Support)', () => {

  test('Deve permitir toggle em modo suporte', async ({ page }) => {
    // 1. Mock da API de Features (GET e POST)
    await page.route('**/api/admin/features', async route => {
      if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          body: JSON.stringify({ fiscal_module_v2: false })
        });
      } else if (route.request().method() === 'POST') {
        const payload = JSON.parse(route.request().postData() || '{}');
        await route.fulfill({
          status: 200,
          body: JSON.stringify({ message: 'Updated', status: payload.is_enabled })
        });
      }
    });

    // 2. Login como Suporte (Com Impersonation)
    await page.goto(`${BASE_URL}/admin/login`);
    await page.evaluate(() => {
      const token = btoa(JSON.stringify({ sub: 'support@mesaflow.com', role: 'owner', impersonator: true }));
      localStorage.setItem('mesaflow_access_token', `fake.${token}.fake`);
      localStorage.setItem('mesaflow_user_role', 'owner');
    });

    // 3. Navegar
    await page.goto(`${BASE_URL}/admin/${SLUG}/settings/features`);

    // 4. Validações de Segurança
    await expect(page.getByText('MODO SUPORTE ATIVO')).toBeVisible();
    
    const toggle = page.getByRole('button', { name: /Alternar Módulo Fiscal/i });
    await expect(toggle).toBeEnabled();

    // 5. Ação de Toggle
    await toggle.click();
    
    // 6. Feedback de Sucesso
    await expect(page.getByText('Funcionalidade ativada!')).toBeVisible();
    
    // Verifica mudança visual do toggle (classe de cor)
    await expect(toggle).toHaveClass(/bg-orange-600/);
  });
});
