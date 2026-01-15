// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 16:30:00
import { test, expect } from '@playwright/test';

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    await page.goto('/admin/hamburgueria-ze/driver');
    const card = page.locator('[data-testid="driver.delivery.order.card"]').first();
    await card.locator('[data-testid="driver.delivery.order.pickup"]').click();
    await expect(page.locator('[data-testid="driver.delivery.active"]')).toBeVisible();
});

test('Test 10: Client Passive Tracking', async ({ page }) => {
    page.on('request', req => {
        if (req.url().includes('osrm')) throw new Error('Client is calculating route!');
    });
    await page.goto('/hamburgueria-ze/menu?order=UUID');
    await expect(page.locator('[data-testid="customer.order.map"]')).toBeVisible();
});
