import { test, expect } from '@playwright/test';

// =============================================================================
// 🛡️ KIOSK SANDBOX SECURITY PROBE
// =============================================================================
// Objetivo: Validar se o middleware impede a fuga do modo Kiosk para o Admin.
// =============================================================================

test.describe('Kiosk Security Sandbox', () => {
  
  test('Deve marcar a sessão com cookie ao entrar no Kiosk', async ({ page }) => {
    // 1. Entra no Kiosk
    await page.goto('/hamburgueria-ze/kiosk');
    
    // 2. Verifica se o cookie foi setado
    const cookies = await page.context().cookies();
    const kioskCookie = cookies.find(c => c.name === 'mf_kiosk_mode');
    
    expect(kioskCookie).toBeDefined();
    expect(kioskCookie?.value).toBe('1');
  });

  test('Deve bloquear navegação para Admin se estiver em modo Kiosk (Trap)', async ({ page }) => {
    // 1. Entra no Kiosk (Seta o cookie)
    await page.goto('/hamburgueria-ze/kiosk');
    
    // 2. Tenta navegar manualmente para o Admin (Simulando ataque de URL)
    await page.goto('/admin/dashboard');
    
    // 3. Deve ser redirecionado de volta ou para a home (NUNCA ficar no admin)
    await expect(page).not.toHaveURL(/\/admin\/dashboard/);
  });

  test('Deve permitir navegação para Menu Público dentro do contexto Kiosk', async ({ page }) => {
    await page.goto('/hamburgueria-ze/kiosk');
    
    // Navegação legítima
    await page.goto('/hamburgueria-ze/menu');
    
    // Deve permitir
    await expect(page).toHaveURL(/\/hamburgueria-ze\/menu/);
  });

  test('Admin sem contexto Kiosk deve acessar normalmente', async ({ page }) => {
    // Limpa cookies para garantir sessão limpa
    await page.context().clearCookies();
    
    await page.goto('/admin/login');
    await expect(page).toHaveURL(/\/admin\/login/);
  });
});

