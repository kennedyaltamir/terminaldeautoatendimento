// Validated via atualizar.py pipeline
import { test, expect } from '@playwright/test';

const BASE_URL = 'http://127.0.0.1:3000';
const SLUG = 'hamburgueria-ze';

test.describe('Feature Flags - Error Handling', () => {

  test('Deve fazer rollback visual em caso de erro na API', async ({ page }) => {
    // 1. Mock de Erro no POST
    await page.route('**/api/admin/features', async route => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ status: 200, body: JSON.stringify({ fiscal_module_v2: false }) });
      } else {
        // Simula erro 500 no servidor
        await route.fulfill({ status: 500, body: JSON.stringify({ detail: 'Erro interno simulado' }) });
      }
    });

    // 2. Login Suporte
    await page.goto(`${BASE_URL}/admin/login`);
    await page.evaluate(() => {
      const token = btoa(JSON.stringify({ sub: 'support@mesaflow.com', role: 'owner', impersonator: true }));
      localStorage.setItem('mesaflow_access_token', `fake.${token}.fake`);
    });

    await page.goto(`${BASE_URL}/admin/${SLUG}/settings/features`);

    // 3. Tentar ativar (Optimistic Update acontece aqui)
    const toggle = page.getByRole('button', { name: /Alternar Módulo Fiscal/i });
    await toggle.click();

    // 4. Validar Erro e Rollback
    await expect(page.getByText('Erro interno simulado')).toBeVisible();
    
    // O toggle deve voltar a estar desativado (posição inicial/cor cinza)
    await expect(toggle).toHaveClass(/bg-gray-700/); 
  });
});
