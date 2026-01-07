// Validated via atualizar.py pipeline
import { test, expect } from '@playwright/test';

const BASE_URL = 'http://127.0.0.1:3000';
const SLUG = 'hamburgueria-ze';

test.describe('Feature Flags - Read Only Mode', () => {
  
  test('Deve exibir flags em modo leitura para usuário comum', async ({ page }) => {
    // 1. Mock da API de Features (GET)
    await page.route('**/api/admin/features', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ fiscal_module_v2: false })
      });
    });

    // 2. Login como Dono (Sem Impersonation)
    await page.goto(`${BASE_URL}/admin/login`);
    await page.evaluate(() => {
      // Simula token sem claim de impersonator
      const token = btoa(JSON.stringify({ sub: 'owner@test.com', role: 'owner', impersonator: false }));
      localStorage.setItem('mesaflow_access_token', `fake.${token}.fake`);
      localStorage.setItem('mesaflow_user_role', 'owner');
    });

    // 3. Navegar para Configurações > Features
    await page.goto(`${BASE_URL}/admin/${SLUG}/settings/features`);

    // 4. Validações Visuais
    await expect(page.getByText('Modo Leitura')).toBeVisible();
    await expect(page.getByText('Módulo Fiscal v2')).toBeVisible();
    
    // 5. Validação de Segurança (Botão Desabilitado)
    const toggle = page.getByRole('button', { name: /Alternar Módulo Fiscal/i });
    await expect(toggle).toBeDisabled();
    
    // Garante que não é clicável
    await expect(toggle).toHaveClass(/opacity-50/);
  });
});
