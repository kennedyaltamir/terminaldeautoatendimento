// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 19:20:00
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

/**
 * Configuração Playwright v3.0 - Global Auth Architecture
 */
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  timeout: 60000,
  
  // Orquestração de dependência de testes
  projects: [
    // 1. Configura o Setup de Autenticação
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/,
    },
    // 2. Configura os testes funcionais dependentes do setup
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Indica o arquivo de estado gerado pelo setup
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
