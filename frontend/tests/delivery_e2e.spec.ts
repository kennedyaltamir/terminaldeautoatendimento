import { test, expect } from '@playwright/test';

/**
 * 🕵️ LOGISTICS E2E: ULTRA FORENSIC EDITION
 * 
 * Objetivo: Diagnóstico total de permissões, estado de GPS e latência de rede.
 * Versão: 8.0 (Deep Logging)
 */

test.describe('Logistics E2E: Happy Path', () => {
  test.describe.configure({ mode: 'serial' });

  test('Fluxo Completo: Coleta -> Entrega -> Conclusão', async ({ page, request, context }) => {
    
    // --- CONFIGURAÇÃO DE LOGS EXTREMOS ---
    const log = (step: string, msg: any) => {
        const timestamp = new Date().toISOString().split('T')[1].split('Z')[0];
        console.log(`[${timestamp}] 🚀 ${step.toUpperCase()}:`, msg);
    };

    page.on('console', msg => log('BROWSER_CONSOLE', `${msg.type()}: ${msg.text()}`));
    page.on('pageerror', err => log('JS_CRASH', err.message));
    
    // Interceptador de Rede Detalhado
    page.on('request', req => {
        if (req.url().includes('/api/')) {
            log('NET_REQ', `>> ${req.method()} ${req.url()}`);
        }
    });

    page.on('response', async res => {
        if (res.url().includes('/api/')) {
            const status = res.status();
            log('NET_RES', `<< ${status} ${res.url()}`);
            if (status >= 400) {
                try {
                    const body = await res.json();
                    log('NET_ERR_BODY', body);
                } catch {
                    log('NET_ERR_RAW', await res.text());
                }
            }
        }
    });

    // --- CONFIGURAÇÃO DE AMBIENTE (GPS & PERMISSÕES) ---
    log('setup', 'Configurando Geocalização e Permissões...');
    await context.grantPermissions(['geolocation']);
    await context.setGeolocation({ latitude: -19.22448, longitude: -44.93548 });

    await page.addInitScript(() => {
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
      // Injeta flag para o frontend saber que está em teste e não bloquear GPS
      (window as any).__MESAFLOW_TEST_MODE__ = true;
    });

    // 1. PREPARAÇÃO DE DADOS (API)
    log('data_setup', 'Autenticando via API para criar massa de dados...');
    const loginRes = await request.post('http://localhost:8000/api/auth/token', {
        form: { username: 'admin@mesaflow.com', password: '123456' }
    });
    
    if (!loginRes.ok()) {
        log('critical_error', 'Falha no login de API. O backend está rodando?');
        expect(loginRes.ok()).toBeTruthy();
    }

    const { access_token } = await loginRes.json();
    const authHeaders = { 'Authorization': `Bearer ${access_token}` };

    log('data_setup', 'Buscando produto para o pedido...');
    const menuRes = await request.get('http://localhost:8000/api/public/hamburgueria-ze/menu');
    const menu = await menuRes.json();
    const product = menu.categories?.[0]?.products?.[0];
    
    if (!product) throw new Error("❌ Cardápio vazio no banco.");

    log('data_setup', `Criando pedido para o produto: ${product.name}`);
    const orderRes = await request.post('http://localhost:8000/api/public/hamburgueria-ze/orders', {
        data: {
            customer_name: "Playwright Forensic",
            customer_phone: "11999999999",
            order_type: "delivery",
            delivery_address: "Rua Forense, 100",
            payment_method: "online",
            items: [{ product_id: product.id, quantity: 1 }]
        }
    });
    const order = await orderRes.json();
    log('data_setup', `Pedido criado: ${order.id}`);

    log('data_setup', 'Movendo pedido para READY (Cozinha)...');
    await request.patch(`http://localhost:8000/api/admin/orders/${order.id}`, {
        headers: authHeaders,
        data: { status: "ready" }
    });

    // 2. TESTE DE UI
    log('ui_login', 'Iniciando fluxo de login visual...');
    await page.goto('/admin/login');
    await page.waitForLoadState('domcontentloaded');
    
    await page.locator('input[name="email"]').fill('admin@mesaflow.com');
    await page.locator('input[name="password"]').fill('123456');
    await page.keyboard.press('Enter');

    log('ui_nav', 'Aguardando Dashboard...');
    await page.waitForURL('**/dashboard', { timeout: 30000 });

    log('ui_nav', 'Navegando para o Painel do Motorista...');
    await page.goto('/admin/hamburgueria-ze/driver');
    await page.waitForLoadState('networkidle');

    // --- INSPEÇÃO DE GPS ---
    log('ui_inspect', 'Verificando estado do GPS na UI...');
    const gpsBadge = page.locator('header p:has-text("GPS")');
    const gpsText = await gpsBadge.innerText();
    log('ui_inspect', `Texto do GPS detectado: ${gpsText}`);
    
    if (gpsText.includes('OFF')) {
        log('ui_warn', 'GPS ainda está OFF. Verificando se há erro de permissão no console...');
    }

    // 3. REFRESH E SINCRONIA
    const refreshBtn = page.locator('button:has(svg.lucide-refresh-cw)');
    log('ui_action', 'Verificando botão de Refresh...');
    
    await expect(refreshBtn).toBeVisible();
    
    log('ui_action', 'Clicando no Refresh e aguardando resposta /delivery/orders...');
    const responsePromise = page.waitForResponse(
        resp => resp.url().includes('/delivery/orders'),
        { timeout: 15000 }
    );
    
    await refreshBtn.click();
    const ordersResponse = await responsePromise;
    log('ui_sync', `Resposta do Refresh: ${ordersResponse.status()}`);

    // 4. LOCALIZAR PEDIDO
    log('ui_inspect', `Procurando card do pedido ${order.id}...`);
    const targetCard = page.locator(`[data-order-id="${order.id}"]`);
    
    try {
        await expect(targetCard).toBeVisible({ timeout: 15000 });
        log('ui_success', 'Pedido encontrado na lista!');
    } catch (e) {
        log('ui_fail', 'Pedido NÃO apareceu. Capturando estado do LocalStorage...');
        const storage = await page.evaluate(() => JSON.stringify(localStorage, null, 2));
        console.log("[DEBUG] LocalStorage State:", storage);
        throw e;
    }

    // 5. COLETA (DISPATCH)
    log('ui_action', 'Iniciando coleta (Pickup)...');
    const pickupBtn = targetCard.getByTestId('driver.delivery.order.pickup');
    
    const dispatchPromise = page.waitForResponse(r => r.url().includes('/dispatch'));
    await pickupBtn.click({ force: true });
    const dispatchRes = await dispatchPromise;
    log('ui_action', `Resposta do Dispatch: ${dispatchRes.status()}`);

    // 6. VALIDAÇÃO DE MAPA
    log('ui_inspect', 'Validando transição para o Mapa...');
    const activePanel = page.getByTestId('driver.delivery.active');
    await expect(activePanel).toBeVisible({ timeout: 15000 });
    
    // Verifica se o mapa (Leaflet) carregou
    const mapContainer = page.locator('.leaflet-container');
    await expect(mapContainer).toBeVisible();
    log('ui_success', 'Mapa renderizado com sucesso.');

    // 7. FINALIZAR
    log('ui_action', 'Finalizando entrega...');
    await page.locator('button:has-text("Finalizar Entrega")').click();
    
    await page.locator('input[type="tel"]').fill('0000');
    const completePromise = page.waitForResponse(r => r.url().includes('/complete'));
    await page.locator('button:has-text("Validar e Finalizar")').click();
    
    const finalRes = await completePromise;
    log('ui_finish', `Status Final: ${finalRes.status()}`);
    
    await expect(activePanel).not.toBeVisible({ timeout: 10000 });
    log('ui_finish', 'Fluxo concluído. Sistema retornou à lista de disponíveis.');
  });
});