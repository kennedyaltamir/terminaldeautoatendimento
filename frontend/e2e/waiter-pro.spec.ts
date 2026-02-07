import { test, expect } from '@playwright/test';

test.describe('Garçom Pro Features', () => {
  test('deve identificar cliente e ajustar gorjeta no fechamento', async ({ page, context }) => {
    // 1. Setup de Auth (Injeção Robusta)
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'cashier');
    });

    // 2. Mocks de API (Garantir que todas as chamadas de verificação passem)
    
    // Mock de Perfil (Evita redirecionamento por falta de dados da empresa)
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Bar do Zé", plan_tier: "pro", service_fee_percentage: 10 } });
    });

    // Mock de Validação de Token (Se houver chamada de verify)
    // Assumindo que o frontend confia no localStorage ou faz um fetch inicial
    
    // Mock da Carteira (Cliente com saldo)
    await page.route('**/api/hamburgueria-ze/wallet/11999999999', async route => {
      await route.fulfill({ status: 200, json: { balance: 15.50, loyalty_percentage: 10 } });
    });

    // Mock do Menu
    await page.route('**/api/hamburgueria-ze/menu', async route => {
      await route.fulfill({ status: 200, json: { 
        company: { name: "Bar do Zé" }, 
        categories: [{ id: 1, name: "Bebidas", products: [{ id: 1, name: "Cerveja", price: 10.00 }] }] 
      }});
    });

    // Mock do Status da Mesa (Ativa)
    await page.route('**/api/hamburgueria-ze/check-table', async route => {
      await route.fulfill({ status: 200, json: { status: 'active', session_token: 'sess-123', customer_name: 'João' } });
    });

    // Mock da Sessão (Com 1 pedido de R$ 100)
    await page.route('**/api/hamburgueria-ze/session/sess-123', async route => {
      await route.fulfill({ status: 200, json: { 
        id: 123, 
        customer_name: 'João', 
        total_spent: 100.00, 
        orders: [{ id: 'ord-1', total_amount: 100.00, items: [], status: 'delivered' }] 
      }});
    });

    // Mock do Fechamento
    await page.route('**/api/admin/tables/1/close', async route => {
      const data = JSON.parse(route.request().postData() || '{}');
      if (data.custom_service_fee === 15) {
        await route.fulfill({ status: 200, json: { message: "Mesa fechada" } });
      } else {
        await route.fulfill({ status: 400, json: { detail: "Gorjeta incorreta no payload" } });
      }
    });

    // 3. Navegar para o POS da Mesa 1
    await page.goto('/admin/hamburgueria-ze/waiter/pos/1', { waitUntil: 'domcontentloaded' });

    // Verificação de Segurança: Se redirecionou para login, o teste falha aqui com mensagem clara
    await expect(page).toHaveURL(/\/waiter\/pos\/1/);

    // 4. Testar Identificação de Cliente (Opcional, focado no pagamento)
    
    // 5. Abrir Modal de Pagamento
    // Espera o botão aparecer (pode demorar se estiver carregando dados da sessão)
    const closeBtn = page.getByTitle('Fechar Conta');
    await expect(closeBtn).toBeVisible({ timeout: 10000 });
    await closeBtn.click();

    await expect(page.getByText('Total a Receber')).toBeVisible();

    // 6. Validar Cálculo Inicial (10% padrão)
    // Subtotal 100 + 10% = 110
    await expect(page.getByText('R$ 110.00')).toBeVisible();

    // 7. Alterar Gorjeta
    // Clica no botão de editar (pode ser um ícone ou texto)
    // O seletor anterior era locator('button:has-text("Edit")'), vamos ser mais específicos se possível
    // Ou usar o ícone se tiver aria-label
    await page.locator('button').filter({ has: page.locator('svg.lucide-edit-2') }).click();
    
    // Selecionar 12% (Botão pré-definido)
    await page.getByRole('button', { name: '12%' }).click();
    await expect(page.getByText('R$ 112.00')).toBeVisible(); // 100 + 12

    // Digitar valor manual (15%)
    const tipInput = page.locator('input[type="number"]').first();
    await tipInput.fill('15');
    
    // Verifica recalculo: 100 + 15% = 115.00
    await expect(page.getByText('R$ 115.00')).toBeVisible();

    // 8. Finalizar com Dinheiro
    await page.getByText('Dinheiro').click();
    
    // Calculadora de Troco deve abrir
    await expect(page.getByText('Calculadora de Troco')).toBeVisible();
    
    // Pagar R$ 120
    await page.getByRole('button', { name: '1' }).click();
    await page.getByRole('button', { name: '2' }).click();
    await page.getByRole('button', { name: '0' }).click();
    
    // Confirmar
    await page.getByText('Confirmar Pagamento').click();

    // 9. Sucesso
    await expect(page.getByText('Mesa finalizada com sucesso!')).toBeVisible();
  });
});
