import { test, expect } from '@playwright/test';

test.describe('Motor de Promoções (Frontend)', () => {
  test.beforeEach(async ({ page }) => {
    // Mock do Menu com um produto de R$ 50.00
    await page.route('**/api/*/menu', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          company: { name: 'Loja de Teste', primary_color: '#ea580c' },
          categories: [{
            id: 1,
            name: 'Lanches',
            products: [{
              id: 100,
              name: 'Hambúrguer Teste',
              price: 50.00,
              is_available: true,
              option_groups: [],
              tags: ['promo']
            }]
          }]
        })
      });
    });

    // Mock de Validação de Cupom Válido (TESTE10)
    await page.route('**/api/*/cart/validate-coupon', async (route) => {
      const payload = route.request().postDataJSON();
      if (payload.code === 'TESTE10') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            valid: true,
            discount_amount: 10.00,
            final_total: 40.00,
            message: 'Cupom aplicado!',
            promotion_id: 'promo-uuid-123'
          })
        });
      } else {
        await route.fulfill({
          status: 400,
          contentType: 'application/json',
          body: JSON.stringify({ detail: 'Cupom expirado ou inválido' })
        });
      }
    });

    await page.goto('/hamburgueria-ze/menu');
  });

  test('deve aplicar um cupom válido e exibir o desconto', async ({ page }) => {
    // 1. Adicionar produto ao carrinho
    await page.getByText('Hambúrguer Teste').click();
    await page.getByRole('button', { name: 'Adicionar' }).click();

    // 2. Abrir Carrinho
    await page.getByRole('button', { name: /Ver Carrinho/ }).click();

    // 3. Aplicar Cupom
    const couponInput = page.getByPlaceholder('CÓDIGO');
    await couponInput.fill('TESTE10');
    await page.getByRole('button', { name: 'Aplicar' }).click();

    // 4. Validar Feedback Visual e Cálculos
    // O resumo financeiro deve mostrar o desconto
    await expect(page.getByText('- R$ 10.00')).toBeVisible();
    await expect(page.getByText('R$ 40.00')).toBeVisible(); 
    
    // CORREÇÃO: A string real exibida no componente é dinâmica
    await expect(page.getByText('Desconto de R$ 10.00 aplicado!')).toBeVisible();
  });

  test('deve exibir erro ao tentar cupom inválido', async ({ page }) => {
    // 1. Adicionar produto
    await page.getByText('Hambúrguer Teste').click();
    await page.getByRole('button', { name: 'Adicionar' }).click();
    await page.getByRole('button', { name: /Ver Carrinho/ }).click();

    // 2. Tentar Cupom Inválido
    await page.getByPlaceholder('CÓDIGO').fill('INVALIDO');
    await page.getByRole('button', { name: 'Aplicar' }).click();

    // 3. Validar Erro
    await expect(page.getByText('Cupom expirado ou inválido')).toBeVisible();
    
    // CORREÇÃO: Usar exact match para não confundir com o label "CUPOM DE DESCONTO"
    await expect(page.getByText('Desconto', { exact: true })).not.toBeVisible();
  });

  test('deve remover o desconto se o carrinho for alterado', async ({ page }) => {
    await page.getByText('Hambúrguer Teste').click();
    await page.getByRole('button', { name: 'Adicionar' }).click();
    await page.getByRole('button', { name: /Ver Carrinho/ }).click();

    // Aplicar cupom
    await page.getByPlaceholder('CÓDIGO').fill('TESTE10');
    await page.getByRole('button', { name: 'Aplicar' }).click();
    await expect(page.getByText('- R$ 10.00')).toBeVisible();

    // Remover item do carrinho
    await page.getByRole('button', { name: 'Remover' }).click();

    // O cupom deve ser invalidado/removido automaticamente pela lógica de useEffect
    await expect(page.getByText('- R$ 10.00')).not.toBeVisible();
    await expect(page.getByText('Carrinho alterado. Valide o cupom novamente.')).toBeVisible();
  });
});
