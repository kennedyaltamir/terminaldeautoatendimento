// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 18:05:00
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

/**
 * Configuração Playwright v2.5 - Intra-Project & Path-Aware
 */
export default defineConfig({
  // Ajustado para olhar a pasta de testes dentro do frontend
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  timeout: 60000,
  use: {
    baseURL: 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 30000,
    navigationTimeout: 45000,
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://127.0.0.1:3000',
    reuseExistingServer: true,
    timeout: 120 * 1000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
