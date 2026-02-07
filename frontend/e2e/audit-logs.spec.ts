import { test, expect } from '@playwright/test';

test.describe('Audit Logs Viewer', () => {
  test('deve exibir logs de auditoria para o dono', async ({ page, context }) => {
    // 1. Injetar Token de Dono E PULAR O TOUR
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'owner');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });

    // 2. Mock Auth
    await page.route('**/api/admin/company/me', async (route) => {
      await route.fulfill({ 
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ name: "Hamburgueria Zé", plan_tier: "pro", owner_email: "admin@teste.com" })
      });
    });

    // 3. Mock Logs API
    await page.route('**/api/admin/audit?limit=50', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: 1,
            user_name: "Admin",
            user_role: "owner",
            action: "create",
            resource: "Product",
            resource_id: "101",
            details: { name: "X-Bacon", price: 25.00 },
            created_at: new Date().toISOString()
          },
          {
            id: 2,
            user_name: "Gerente",
            user_role: "manager",
            action: "delete",
            resource: "Order",
            resource_id: "555",
            details: null,
            created_at: new Date().toISOString()
          }
        ])
      });
    });

    // 4. Navegar para a página de Auditoria
    await page.goto('/admin/hamburgueria-ze/audit');

    // 5. Verificar Título
    await expect(page.getByText('Auditoria & Segurança')).toBeVisible();

    // 6. Verificar Dados na Tabela
    await expect(page.getByText('create')).toBeVisible(); 
    await expect(page.getByText('delete')).toBeVisible(); 

    // 7. Verificar Detalhes (JSON)
    // Como o tooltip pode ser chato de testar visualmente (hover), verificamos se o dado existe no DOM.
    // O texto "X-Bacon" deve estar presente no HTML, mesmo que oculto.
    const detailsText = page.getByText('X-Bacon');
    await expect(detailsText).toBeAttached(); 
    
    // Opcional: Tentar forçar o hover para garantir que a interação existe, mas sem bloquear o teste se a animação falhar
    const icon = page.locator('.group').first();
    await icon.hover();
  });
});
