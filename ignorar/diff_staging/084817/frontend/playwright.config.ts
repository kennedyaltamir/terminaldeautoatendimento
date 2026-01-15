# DOMAIN: FRONTEND
# LAST_MODIFIED: 2026-01-15 17:15:00
import { defineConfig, devices } from '@playwright/test';

/**
 * Configuração Playwright v2 - Cross-Directory Aware
 * Permite a execução de testes localizados fora da pasta frontend/
 */
export default defineConfig({
  // Permite que o Playwright procure testes em qualquer lugar do projeto
  // desde que o comando especifique o arquivo
  testDir: '../tests/frontend',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  timeout: 120000,
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
