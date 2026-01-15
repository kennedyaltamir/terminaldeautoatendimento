// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 18:25:00
import { defineConfig, devices } from '@playwright/test';

/**
 * Configuração Playwright v2.3 - Intra-Project Mode
 * Os testes agora residem dentro da pasta do projeto frontend para
 * garantir a resolução correta dos módulos do node_modules.
 */
export default defineConfig({
  testDir: './tests', // Busca testes na pasta interna
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
