import { test, expect } from '@playwright/test';

test.describe('Driver App Full Lifecycle', () => {
  test('deve realizar o fluxo completo: Retirar -> Navegar -> Finalizar', async ({ page, context }) => {
    
    // 1. SETUP: Mocks de Ambiente e Auth
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-driver-token');
      window.localStorage.setItem('mesaflow_user_role', 'driver');
      
      // Mock de Geolocalização para não travar pedindo permissão
      const mockGeolocation = {
        getCurrentPosition: (success: any) => success({ coords: { latitude: -23.55, longitude: -46.63 } }),
        watchPosition: (success: any) => success({ coords: { latitude: -23.55, longitude: -46.63 } })
      };
      (navigator as any).geolocation = mockGeolocation;
    });

    // 2. Mocks de API
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Logística Zé", plan_tier: "pro" } });
    });

    // Mock Inicial: 1 Pedido Pronto (A Retirar)
    await page.route('**/api/admin/delivery/orders', async route => {
      await route.fulfill({ 
        status: 200, 
        json: [
          { 
            id: 'ord-ready', 
            status: 'ready', 
            customer_name: 'Cliente Retirada', 
            delivery_address: 'Rua A, 100',
            customer_phone: '11999999999',
            payment_method: 'online',
            total_amount: 50.00,
            delivery_code: '1234'
          }
        ] 
      });
    });

    // 3. Navegar para o App do Motorista
    await page.goto('/admin/hamburgueria-ze/driver');

    // --- ETAPA 1: RETIRADA ---
    await expect(page.getByText('A Retirar (1)')).toBeVisible();
    await expect(page.getByText('Cliente Retirada')).toBeVisible();

    // Mock da ação de "Pegar Pedido" (Dispatch)
    await page.route('**/api/admin/delivery/orders/ord-ready/dispatch', async route => {
      await route.fulfill({ status: 200, json: { message: "Despachado" } });
    });

    // --- ATUALIZAÇÃO DO MOCK ANTECIPADA ---
    // Atualizar Mock para simular que o pedido agora está "Em Rota"
    // Fazemos isso ANTES do clique para que o fetchMyOrders() chamado pelo clique já pegue o novo estado
    await page.route('**/api/admin/delivery/orders', async route => {
      await route.fulfill({ 
        status: 200, 
        json: [
          { 
            id: 'ord-ready', 
            status: 'delivering', // Mudou status
            customer_name: 'Cliente Retirada', 
            delivery_address: 'Rua A, 100',
            customer_phone: '11999999999',
            payment_method: 'online',
            total_amount: 50.00,
            delivery_code: '1234'
          }
        ] 
      });
    });

    // Clicar em Pegar Pedido
    await page.getByText('Pegar Pedido').click();
    await expect(page.getByText('Rota iniciada!')).toBeVisible();

    // --- ETAPA 2: EM ROTA & FERRAMENTAS ---
    
    // Vamos clicar na aba "Em Rota" para garantir
    await page.getByText('Em Rota').click();
    
    // Verificar botões de ação
    await expect(page.getByText('Waze')).toBeVisible();
    await expect(page.getByText('WhatsApp')).toBeVisible();

    // Testar Deep Link (Waze)
    // Interceptamos window.open
    const page1Promise = page.waitForEvent('popup');
    await page.getByText('Waze').click();
    const popup = await page1Promise;
    // Verifica se a URL do popup contém waze
    expect(popup.url()).toContain('waze.com');
    await popup.close();

    // --- ETAPA 3: FINALIZAÇÃO (POD) ---
    
    // Clicar em Confirmar Entrega
    await page.getByText('Confirmar Entrega').click();
    
    // Modal deve abrir
    await expect(page.getByText('Segurança de Entrega')).toBeVisible();

    // Digitar Código Errado (Teste de Validação de UI - O botão fica desabilitado se < 4 chars)
    const input = page.locator('input[type="tel"]');
    await input.fill('12');
    await expect(page.getByRole('button', { name: 'Validar e Finalizar' })).toBeDisabled();

    // Digitar Código Completo
    await input.fill('1234');
    await expect(page.getByRole('button', { name: 'Validar e Finalizar' })).toBeEnabled();

    // Mock da Finalização
    await page.route('**/api/admin/delivery/orders/ord-ready/complete', async route => {
      const data = JSON.parse(route.request().postData() || '{}');
      if (data.code === '1234') {
        await route.fulfill({ status: 200, json: { message: "Entregue" } });
      } else {
        await route.fulfill({ status: 403, json: { detail: "Código inválido" } });
      }
    });

    // Finalizar
    await page.getByRole('button', { name: 'Validar e Finalizar' }).click();

    // Sucesso
    await expect(page.getByText('Entrega finalizada!')).toBeVisible();
  });
});
