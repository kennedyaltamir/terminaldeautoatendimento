import { test, expect } from '@playwright/test';

test.describe('Skeleton Loading UX', () => {
  // Mock Genérico de Empresa para Layout
  const mockCompany = { name: "Hamburgueria Zé", slug: "hamburgueria-ze", plan_tier: "pro", owner_email: "admin@teste.com" };

  test.beforeEach(async ({ page, context }) => {
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-token');
      window.localStorage.setItem('mesaflow_user_role', 'owner');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });

    await page.route('**/api/admin/company/me', route => route.fulfill({ status: 200, json: mockCompany }));
  });

  test('deve exibir skeleton no dashboard antes do conteúdo real', async ({ page }) => {
    await page.route('**/api/admin/metrics*', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        json: { total_revenue: 100, total_orders: 1, average_ticket: 100, top_products: [], sales_chart: [], sales_by_hour: [], product_performance: [], ticket_evolution: [] }
      });
    });

    await page.goto('/admin/hamburgueria-ze/dashboard');
    const skeletons = page.locator('.animate-pulse');
    await expect(skeletons.first()).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Faturamento')).toBeVisible({ timeout: 15000 });
    await expect(skeletons.first()).not.toBeVisible();
  });

  test('deve exibir skeleton no cardápio antes do conteúdo real', async ({ page }) => {
    await page.route('**/api/hamburgueria-ze/menu', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        json: { company: mockCompany, categories: [{ id: 1, name: "Lanches", products: [] }] }
      });
    });

    await page.goto('/admin/hamburgueria-ze/menu');
    const skeletons = page.locator('.animate-pulse');
    await expect(skeletons.first()).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Gestão de Produtos')).toBeVisible({ timeout: 15000 });
    await expect(skeletons.first()).not.toBeVisible();
  });

  test('deve exibir skeleton no estoque antes do conteúdo real', async ({ page }) => {
    await page.route('**/api/admin/inventory/ingredients', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({ status: 200, json: [] });
    });

    await page.goto('/admin/hamburgueria-ze/inventory');
    const skeletons = page.locator('.animate-pulse');
    await expect(skeletons.first()).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Gestão de Estoque')).toBeVisible({ timeout: 15000 });
    await expect(skeletons.first()).not.toBeVisible();
  });
});
