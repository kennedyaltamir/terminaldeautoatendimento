// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 17:55:00
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

/**
 * Configuração Playwright v2.2 - Robust Path Mapping
 */
export default defineConfig({
  // Garante que o Playwright procure os testes na pasta correta na raiz
  testDir: path.resolve(__dirname, '../tests/frontend'),
  // Procura por arquivos que terminem com .spec.ts ou .test.ts
  testMatch: '**/*.spec.ts',
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
    actionTimeout: 15000,
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
