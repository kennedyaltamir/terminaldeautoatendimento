import { test, expect } from '@playwright/test';

test.describe('Fiscal Settings', () => {
  test('deve salvar configurações fiscais', async ({ page, context }) => {
    // 1. Injetar Token de Dono e Pular Tour
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'owner');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });

    // 2. Mock Auth
    await page.route('**/api/admin/company/me', async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ 
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ 
            name: "Hamburgueria Zé", 
            plan_tier: "pro", 
            owner_email: "admin@teste.com",
            cnpj: null 
          })
        });
      } else if (route.request().method() === 'PATCH') {
        // Mock do salvamento
        await route.fulfill({ 
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ success: true })
        });
      }
    });

    // 3. Navegar
    await page.goto('/admin/hamburgueria-ze/settings');

    // 4. Clicar na aba Fiscal
    await page.getByText('Fiscal (NFC-e)').click();

    // 5. Preencher CNPJ (Usando Placeholder para maior robustez)
    const cnpjInput = page.getByPlaceholder('00000000000191');
    await expect(cnpjInput).toBeVisible();
    await cnpjInput.fill('12345678000199');

    // 6. Salvar (Clicando no botão inferior do formulário)
    // Usamos .last() porque o botão do header também tem o mesmo texto
    await page.getByText('Salvar Alterações').last().click();

    // 7. Verificar Toast de Sucesso
    await expect(page.getByText('Configurações salvas com sucesso!')).toBeVisible();
  });
});
