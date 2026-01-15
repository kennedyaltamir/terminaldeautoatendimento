// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 20:10:00
import { test, expect } from '@playwright/test';

/**
 * 🧪 Testes de Logística E2E (L6 - Hardened)
 * 
 * MODO SERIAL: Obrigatório pois os testes alteram o estado global do Tenant.
 * Evita que o Teste 10 tente ler um pedido que o Teste 9 já despachou.
 */
test.describe.configure({ mode: 'serial' });

test('Test 9: Driver Transitions to Map', async ({ page }) => {
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // 1. Localiza o card de pedido disponível
    const card = page.getByTestId('driver.delivery.order.card').first();
    
    // Aguarda visibilidade com timeout estendido para suportar latência da API em ambiente dev
    await expect(card).toBeVisible({ 
        timeout: 30000,
        message: "FALHA: Nenhum pedido disponível para coleta. Execute 'python scripts/maintenance/seed_ui_states.py'."
    });
    
    // 2. Prepara a captura da resposta de rede para garantir sincronia determinística
    const dispatchPromise = page.waitForResponse(resp => 
        resp.url().includes('/dispatch') && resp.status() === 200
    );

    // 3. Executa o pickup (force: true para ignorar overlays de onboarding/joyride)
    await card.getByTestId('driver.delivery.order.pickup').click({ force: true });
    
    // 4. Aguarda a confirmação do backend antes de prosseguir para a asserção visual
    await dispatchPromise;

    // 5. Valida transição para modo navegação ativa
    // Aumentado timeout para 15s para suportar carregamento do mapa Leaflet
    await expect(page.getByTestId('driver.delivery.active')).toBeVisible({ timeout: 15000 });
});

test('Test 10: Client Passive Tracking', async ({ page }) => {
    // Interceptação de rede para garantir conformidade arquitetural (Cliente Passivo)
    page.on('request', req => {
        const url = req.url();
        if (url.includes('osrm') || url.includes('google.com/maps/dir')) {
            throw new Error(`VIOLAÇÃO ARQUITETURAL: Cliente calculando rota localmente! URL: ${url}`);
        }
    });

    // 1. Obtém um pedido da lista do entregador para rastreio
    await page.goto('/admin/hamburgueria-ze/driver');
    
    // Lógica de seleção resiliente: READY ou DELIVERING
    const activeCard = page.getByTestId('driver.delivery.active');
    const availableCard = page.getByTestId('driver.delivery.order.card').first();

    let orderId: string | null = null;

    if (await availableCard.isVisible()) {
        orderId = await availableCard.getAttribute('data-order-id');
    } else if (await activeCard.isVisible()) {
        // Fallback: Se o Teste 9 deixou um pedido ativo, usamos ele para o rastreio do cliente
        orderId = await activeCard.locator('[data-order-id]').first().getAttribute('data-order-id');
    }

    if (!orderId) {
        throw new Error("Abortando: Nenhum pedido encontrado para rastreamento (READY ou DELIVERING).");
    }

    // 2. Navega para a visão do cliente
    await page.goto(`/hamburgueria-ze/menu?order=${orderId}`);
    
    // 3. Valida renderização da UI de status e stepper
    await expect(page.locator('h1')).toContainText('Olá', { timeout: 15000 });
    await expect(page.getByTestId('customer.order.stepper')).toBeVisible();
});
