import { test as setup, expect } from '@playwright/test';
import path from 'path';

const STORAGE_STATE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate admin', async ({ page }) => {
  await page.goto('/admin/login');
  
  await page.waitForLoadState('networkidle');

  await page.fill('input[name="email"]', 'admin@mesaflow.com');
  await page.fill('input[name="password"]', '123456');
  
  const submitBtn = page.getByRole('button', { name: /ENTRAR NO SISTEMA/i });
  await expect(submitBtn).toBeEnabled();
  
  await submitBtn.click();

  await page.waitForURL('**/dashboard', { timeout: 30000 });
  await page.waitForLoadState('networkidle');

  await page.evaluate(() => {
    localStorage.setItem('mesaflow_tour_completed', 'true');
  });

  await page.context().storageState({ path: STORAGE_STATE });
});
