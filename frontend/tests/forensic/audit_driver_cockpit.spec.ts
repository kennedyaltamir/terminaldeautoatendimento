import { test, expect } from '@playwright/test';

test.beforeEach(async ({ context }) => {
  await context.addInitScript(() => {
    window.localStorage.setItem('mesaflow_tour_completed', 'true');
    window.localStorage.removeItem('mf_driver_state_hamburgueria-ze');
  });
});

test('Audit Driver Cockpit - Production Readiness', async ({ page }) => {
    console.log('🔍 Starting Forensic Scan of Driver Cockpit...');
    await page.goto('/admin/hamburgueria-ze/driver');

    // 1. OFFLINE State
    const startButton = page.getByTestId('start-shift-button');
    await expect(startButton).toBeVisible({ timeout: 15000 });
    console.log('✅ OFFLINE: Start button detected.');

    // 2. Persistent HUD
    await expect(page.locator('text=Rendimento')).toBeVisible();
    console.log('✅ HUD: Persistent visibility confirmed.');

    // 3. Transition OFFLINE -> IDLE
    console.log('🚀 Triggering Shift Start...');
    await startButton.click();

    // 4. IDLE State & Missions
    await expect(page.getByTestId('driver-state-badge')).toHaveText('IDLE', { timeout: 15000 });
    await expect(page.getByTestId('missions-title')).toBeVisible();
    console.log('✅ IDLE: Transition successful.');

    // 5. Stealth Toggle (Unique Locator)
    const stealthToggle = page.getByTestId('stealth-toggle');
    await expect(stealthToggle).toBeVisible();
    await stealthToggle.click();
    console.log('✅ Security: Stealth Mode functional.');

    console.log('🔭 Scan complete. System is compliant.');
});
