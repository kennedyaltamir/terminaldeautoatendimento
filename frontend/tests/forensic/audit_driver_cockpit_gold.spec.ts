import { test, expect, Page } from '@playwright/test';

const TARGET_URL = '/admin/hamburgueria-ze/driver';

test.describe('Driver Cockpit Forensic Audit', () => {
  
  test.beforeEach(async ({ context }) => {
    await context.grantPermissions(['geolocation']);
    await context.setGeolocation({ latitude: -23.5505, longitude: -46.6333 });
    
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'mock-token-forensic');
      window.localStorage.setItem('mesaflow_user_role', 'driver');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });
  });

  test('Audit: Professional Logistics Lifecycle', async ({ page }: { page: Page }) => {
    await page.goto(TARGET_URL);
    await page.waitForLoadState('networkidle');
    
    // Check Header Vitals
    const header = page.locator('header');
    await expect(header).toBeVisible();

    // Check Bottom Nav Presence
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();
    await expect(nav.locator('button')).toHaveCount(4);

    // Click Rota Tab explicitly to ensure state visibility
    await page.locator('button').filter({ has: page.locator('svg.lucide-map') }).click();

    const startBtn = page.locator('button:has-text("Iniciar Trabalho")');
    if (await startBtn.isVisible()) {
      await startBtn.click();
      await expect(page.locator('text=Buscando Missões').or(page.locator('text=ACEITAR ROTA'))).toBeVisible({ timeout: 15000 });
    }
  });
});

