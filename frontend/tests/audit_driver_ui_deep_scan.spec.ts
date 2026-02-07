import { test, expect, Page, BrowserContext, Route } from '@playwright/test';

const TARGET_URL = '/admin/hamburgueria-ze/driver';

test.describe('Driver Cockpit Forensic Audit (Diamond Grade)', () => {
  test.use({
    viewport: { width: 390, height: 844 },
    hasTouch: true,
    geolocation: { latitude: -23.5505, longitude: -46.6333 },
    permissions: ['geolocation'],
  });

  test.beforeEach(async ({ context }: { context: BrowserContext }) => {
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'mock-driver-token-production');
      window.localStorage.setItem('mesaflow_user_role', 'driver');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
      window.localStorage.removeItem('mf_driver_state_hamburgueria-ze');
    });
  });

  test('Validation: Comprehensive Logistics Loop', async ({ page }: { page: Page }) => {
    await page.goto(TARGET_URL, { waitUntil: 'networkidle' });

    // Handle Shift Start
    const startBtn = page.getByTestId('start-shift-button');
    if (await startBtn.isVisible()) {
      await startBtn.click();
      await expect(page.locator('text=Buscando Missões')).toBeVisible({ timeout: 10000 });
    }

    // Mock API for orders
    await page.route('**/api/admin/hamburgueria-ze/orders', async (route: Route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify([{
                id: 'ord-forensic-001',
                customer_name: 'Auditoria Forense',
                total_amount: 5000,
                delivery_address: 'Av. Paulista, 1000',
                status: 'ready',
                order_type: 'delivery',
                driver_id: null
            }])
        });
    });

    const refreshBtn = page.locator('button').filter({ has: page.locator('svg.lucide-refresh-cw') });
    if (await refreshBtn.isVisible()) await refreshBtn.click();

    // Mission Acceptance
    const acceptBtn = page.getByTestId('btn-accept-route');
    await expect(acceptBtn).toBeVisible({ timeout: 15000 });
    const box = await acceptBtn.boundingBox();
    if (box) {
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
      await page.mouse.down();
      await page.waitForTimeout(1600);
      await page.mouse.up();
    }

    // Navigation Verification
    await expect(page.locator('.leaflet-container')).toBeVisible({ timeout: 15000 });
    const arrivedBtn = page.getByTestId('btn-arrived');
    await expect(arrivedBtn).toBeVisible();
    await arrivedBtn.click();

    // POD Logic
    await expect(page.getByText('Fim da Rota')).toBeVisible();
    for (const num of ['1', '2', '3', '4']) {
      await page.getByRole('button', { name: num, exact: true }).click();
    }
    await page.getByRole('button', { name: 'CONCLUIR ENTREGA' }).click();

    // Success Assert
    await expect(page.getByText('Missão Finalizada')).toBeVisible({ timeout: 15000 });
  });
});
