// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 19:15:00
import { test as setup } from '@playwright/test';
import path from 'path';

const STORAGE_STATE = path.join(__dirname, '../.auth/admin.json');

/**
 * 🔐 AUTH SETUP: Real Admin Login
 * Realiza o login real uma única vez para gerar um estado de sessão válido
 * que será reutilizado por todos os testes subsequentes.
 */
setup('authenticate admin', async ({ page }) => {
  await page.goto('/admin/login');

  // Preenche credenciais reais conforme o seed do banco
  await page.fill('input[name="email"]', 'admin@mesaflow.com');
  await page.fill('input[name="password"]', '123456');
  
  // Clica no botão de entrada
  await page.click('button[type="submit"]');

  // Aguarda o redirecionamento para o dashboard para confirmar sucesso
  await page.waitForURL('**/dashboard');

  // Salva o estado (Cookies + LocalStorage) para um arquivo
  await page.context().storageState({ path: STORAGE_STATE });
});
