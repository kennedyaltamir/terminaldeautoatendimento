// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 19:30:00
import { test as setup } from '@playwright/test';
import path from 'path';

const STORAGE_STATE = path.join(__dirname, '../.auth/admin.json');

/**
 * 🔐 AUTH SETUP: Real Admin Login & Session Preparation
 */
setup('authenticate admin', async ({ page }) => {
  await page.goto('/admin/login');

  await page.fill('input[name="email"]', 'admin@mesaflow.com');
  await page.fill('input[name="password"]', '123456');
  await page.click('button[type="submit"]');

  // Garante que o login foi processado pelo backend e o redirecionamento ocorreu
  await page.waitForURL('**/dashboard');

  // 🛡️ BLOQUEIO DE JOYRIDE: Injeta a flag de tour concluído no localStorage 
  // para evitar que o overlay de onboarding bloqueie os cliques nos testes.
  await page.evaluate(() => {
    localStorage.setItem('mesaflow_tour_completed', 'true');
  });

  // Salva Cookies + LocalStorage (incluindo o tour_completed)
  await page.context().storageState({ path: STORAGE_STATE });
});
