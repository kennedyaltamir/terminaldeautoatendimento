// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 17:35:00
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

/**
 * Configuração Playwright v3.1 - Sintaxe Corrigida
 */
export default defineConfig({
  testDir: path.resolve(__dirname, './tests'),
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  timeout: 60000,
  
  projects: [
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        storageState: path.resolve(__dirname, './.auth/admin.json'),
      },
      dependencies: ['setup'],
    },
  ],

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
});
