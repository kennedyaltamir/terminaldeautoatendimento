/**
 * 🕵️ MESAFLOW FORENSIC AUDIT: DRIVER UI DEEP SCAN
 * Domain: Logistics / Quality Assurance
 * Type: End-to-End (E2E) Playwright Test
 * 
 * Execution Context:
 * This script must be executed from the root or frontend directory where @playwright/test is installed.
 * Command: npx playwright test tests/forensic/audit_driver_ui_deep_scan.spec.ts --headed
 */

import { test, expect, Page, BrowserContext, Route } from '@playwright/test';

const TARGET_URL = '/admin/hamburgueria-ze/driver';
const MOCK_TOKEN = 'mock-driver-token-production';

test.describe('Driver Cockpit Forensic Audit (Production Grade)', () => {
  // Configuração de emulação de dispositivo móvel (iPhone 12/13 Pro dimensions)
  test.use({
    viewport: { width: 390, height: 844 },
    hasTouch: true,
    geolocation: { latitude: -23.5505, longitude: -46.6333 },
    permissions: ['geolocation'],
  });

  test.beforeEach(async ({ context }: { context: BrowserContext }) => {
    // Injeção de estado autenticado para bypass de login e setup de ambiente
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'mock-driver-token-production');
      window.localStorage.setItem('mesaflow_user_role', 'driver');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
      // Limpa estado anterior para garantir teste limpo (Idempotência)
      window.localStorage.removeItem('mf_driver_state_hamburgueria-ze');
      console.log('🛡️ [FORENSIC] Environment injected successfully.');
    });
  });

  test('Full Operational Cycle: Shift -> Mission -> Completion -> Idle', async ({ page }: { page: Page }) => {
    console.log('🔍 [STEP 1] Initializing Driver Cockpit...');
    
    // 1. Acesso ao Cockpit
    await page.goto(TARGET_URL, { waitUntil: 'networkidle' });

    // 2. Início de Turno (Se estiver offline)
    const startBtn = page.getByTestId('start-shift-button');
    if (await startBtn.isVisible()) {
      console.log('⚙️ [ACTION] Starting Shift...');
      await startBtn.click();
      // Aguarda transição para estado IDLE (Radar)
      await expect(page.locator('text=Buscando Missões')).toBeVisible({ timeout: 10000 });
    }

    // 3. Injeção de Pedido Mock (Simulação de WebSocket/API)
    console.log('💉 [INJECTION] Mocking Order Data...');
    await page.route('**/api/admin/hamburgueria-ze/orders', async (route: Route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify([{
                id: 'ord-forensic-001',
                customer_name: 'Auditoria Forense',
                total_amount: 5000,
                delivery_address: 'Av. Paulista, 1000',
                status: 'ready',
                order_type: 'delivery',
                driver_id: null
            }])
        });
    });

    // Força um refresh para pegar o pedido mockado
    const refreshBtn = page.locator('button').filter({ has: page.locator('svg.lucide-refresh-cw') });
    if (await refreshBtn.isVisible()) {
        await refreshBtn.click();
    }

    // 4. Aceite de Missão (Hold Button)
    console.log('👆 [INTERACTION] Executing Hold-to-Accept...');
    const acceptBtn = page.getByTestId('btn-accept-route');
    await expect(acceptBtn).toBeVisible({ timeout: 15000 });

    const box = await acceptBtn.boundingBox();
    if (box) {
      // Simula pressão longa (Hold)
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
      await page.mouse.down();
      await page.waitForTimeout(1500); // Tempo do hold
      await page.mouse.up();
    }

    // 5. Validação de Estado: EM ROTA
    console.log('🗺️ [VERIFICATION] Validating Map State...');
    await expect(page.locator('.leaflet-container')).toBeVisible({ timeout: 15000 });
    await expect(page.getByTestId('control-deck')).toBeVisible();

    // 6. Chegada ao Destino
    console.log('📍 [ACTION] Reporting Arrival...');
    // Se o botão de "Cheguei" não estiver visível, pode ser necessário iniciar a navegação primeiro
    const arrivedBtn = page.getByTestId('btn-arrived');
    if (await arrivedBtn.isVisible()) {
        await arrivedBtn.click();
    } else {
        const navBtn = page.getByTestId('btn-start-navigation');
        const navBox = await navBtn.boundingBox();
        if (navBox) {
            await page.mouse.move(navBox.x + navBox.width / 2, navBox.y + navBox.height / 2);
            await page.mouse.down();
            await page.waitForTimeout(1500);
            await page.mouse.up();
        }
        // Agora o botão de chegada deve estar visível
        await expect(page.getByTestId('btn-arrived')).toBeVisible();
        await page.getByTestId('btn-arrived').click();
    }

    // 7. Validação de POD (Proof of Delivery)
    console.log('🔐 [SECURITY] Inputting POD Code...');
    await expect(page.getByText('Fim da Rota')).toBeVisible();
    
    // Digita o código 1234
    await page.getByRole('button', { name: '1' }).click();
    await page.getByRole('button', { name: '2' }).click();
    await page.getByRole('button', { name: '3' }).click();
    await page.getByRole('button', { name: '4' }).click();

    // Confirma entrega
    await page.getByRole('button', { name: 'CONCLUIR ENTREGA' }).click();

    // 8. Tela de Sucesso
    console.log('🎉 [SUCCESS] Mission Complete Screen Verified.');
    await expect(page.getByText('Missão Cumprida!')).toBeVisible();

    // 9. Retorno ao Radar (Ciclo Fechado)
    // Aguarda o timer de auto-dismiss ou clica para pular
    await page.waitForTimeout(6000);
    await expect(page.locator('text=Buscando Missões')).toBeVisible();
    
    console.log('✅ [AUDIT] Full Cycle Completed Successfully.');
  });
});

