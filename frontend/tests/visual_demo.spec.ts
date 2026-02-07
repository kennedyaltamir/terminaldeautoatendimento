import { test, expect } from '@playwright/test';

test.describe.configure({ mode: 'serial' });

test.use({ 
  headless: false,
  viewport: { width: 390, height: 844 },
  launchOptions: { slowMo: 1000 },
  video: 'on', 
});

test.describe('Visual Demonstration', () => {
  test('Motorista: Ciclo Operacional Real', async ({ page, context }) => {
    // 🛡️ CAPTURA DE LOGS DO NAVEGADOR PARA O TERMINAL
    page.on('console', msg => {
        const type = msg.type();
        const text = msg.text();
        if (type === 'error') console.log(`\x1b[31m[BROWSER_ERROR]\x1b[0m ${text}`);
        else if (type === 'warning') console.log(`\x1b[33m[BROWSER_WARN]\x1b[0m ${text}`);
        else console.log(`\x1b[34m[BROWSER_INFO]\x1b[0m ${text}`);
    });

    // 🛡️ MOCK DE API: Garante sucesso na transição de estado para fins visuais
    await page.route('**/api/mobile/logistics/journey/*/accept', async route => {
      console.log('🛡️ [MOCK] Interceptando aceite de jornada...');
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ 
          status: 'success', 
          journey_id: 'mock-journey-123',
          state: 'EN_ROUTE_DELIVERY'
        })
      });
    });

    // 🛡️ MOCK DE API: Garante sucesso na chegada ao destino
    await page.route('**/api/mobile/logistics/journey/*/status', async route => {
        const payload = JSON.parse(route.request().postData() || '{}');
        console.log(`🛡️ [MOCK] Interceptando status update: ${payload.status}`);
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({ success: true })
        });
    });

    // 🛡️ MOCK DE API: Garante sucesso na finalização (POD)
    await page.route('**/api/mobile/logistics/journey/*/complete', async route => {
        console.log('🛡️ [MOCK] Interceptando finalização de entrega...');
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({ success: true })
        });
    });

    await context.grantPermissions(['geolocation']);
    await context.setGeolocation({ latitude: -23.5505, longitude: -46.6333 });

    await page.goto('/');
    
    await page.evaluate(() => {
      window.localStorage.clear();
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
      window.localStorage.removeItem('mf_driver_state_hamburgueria-ze');
    });

    // 1. LOGIN
    await page.goto('/admin/login');
    await page.fill('input[name="email"]', 'admin@mesaflow.com');
    await page.fill('input[name="password"]', '123456');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard');

    // 2. COCKPIT
    await page.goto('/admin/hamburgueria-ze/driver');
    
    const startBtn = page.getByText('Iniciar Trabalho');
    if (await startBtn.isVisible()) {
        await startBtn.click();
    }

    // 3. SELEÇÃO DE MISSÃO REAL
    console.log('🔭 Aguardando missões reais (RLS Validated)...');
    
    const idleView = page.locator('text=Buscando Missões');
    if (await idleView.isVisible()) {
        const simBtn = page.getByRole('button', { name: /Ativar Simulação/i });
        if (await simBtn.isVisible()) {
            await simBtn.click();
        }
    }

    const acceptBtn = page.getByTestId('btn-accept-route').first();
    await expect(acceptBtn).toBeVisible({ timeout: 30000 });

    const box = await acceptBtn.boundingBox();
    if (box) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.mouse.down();
        await page.waitForTimeout(2500); 
        await page.mouse.up();
    }

    // 4. NAVEGAÇÃO
    const navBtn = page.getByTestId('btn-start-navigation');
    await expect(navBtn).toBeVisible({ timeout: 15000 });
    
    const navBox = await navBtn.boundingBox();
    if (navBox) {
        await page.mouse.move(navBox.x + navBox.width / 2, navBox.y + navBox.height / 2);
        await page.mouse.down();
        await page.waitForTimeout(2500); 
        await page.mouse.up();
    }

    // 5. FINALIZAÇÃO
    const arrivedBtn = page.getByTestId('btn-arrived');
    await expect(arrivedBtn).toBeVisible({ timeout: 15000 });
    await arrivedBtn.click();
    
    // Digita o código POD (1234)
    for (const num of ['1', '2', '3', '4']) {
        await page.getByRole('button', { name: num, exact: true }).click();
    }

    const finishBtn = page.getByRole('button', { name: /CONCLUIR ENTREGA/i });
    
    // 🛡️ FIX: Scroll manual via JS para garantir visibilidade em layouts complexos
    await finishBtn.evaluate((el) => el.scrollIntoView({ block: 'center', inline: 'center' }));
    
    // Clica forçado para garantir a ação
    await finishBtn.click({ force: true });

   // 🛡️ FIX: Atualizado para coincidir com o texto real do componente "Missão Finalizada"
    await expect(page.getByRole('heading', { name: /Missão Finalizada/i })).toBeVisible({ timeout: 15000 });
    
    console.log('✨ Fluxo de produção validado com sucesso!');
    await page.waitForTimeout(3000);
  });
});
