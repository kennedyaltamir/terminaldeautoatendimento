import { test, expect } from '@playwright/test';

test('Fluxo Kiosk: Deve gerar link SmartPOS correto', async ({ context, page }) => {
  // 1. Mock do User Agent (Stone POS)
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'userAgent', {
      value: 'Mozilla/5.0 (Linux; Android 10; Stone POS) AppleWebKit/537.36',
      configurable: true
    });
  });

  // 2. Mock do window.location para capturar o Intent
  // Usamos um setter customizado para interceptar a atribuição
  await page.addInitScript(() => {
    let _href = '';
    Object.defineProperty(window, 'location', {
      set: (val) => { _href = val; (window as any).__intentUrl = val; },
      get: () => ({ href: _href }),
      configurable: true
    });
  });

  // 3. Acessar Menu em modo Kiosk
  await page.goto('/hamburgueria-ze/menu?kiosk=true', { waitUntil: 'domcontentloaded' });

  // 4. Adicionar Produto
  await page.getByText('X-Bacon').first().click();

  // Tenta lidar com o modal se ele aparecer (Race Condition)
  const addBtn = page.getByRole('button', { name: /^Adicionar/i });
  const cartBtn = page.getByRole('button', { name: /Ver Carrinho/i });

  // Espera um dos dois aparecer
  await Promise.race([
    addBtn.waitFor({ state: 'visible' }).catch(() => {}),
    cartBtn.waitFor({ state: 'visible' }).catch(() => {})
  ]);

  if (await addBtn.isVisible()) {
    await addBtn.click();
    await cartBtn.waitFor({ state: 'visible' });
  }

  // 5. Ir para Checkout
  await cartBtn.click();

  // 6. Verificar se campos de Delivery sumiram (Kiosk = Takeout)
  await expect(page.getByPlaceholder('Endereço de Entrega')).toBeHidden();

  // 7. Selecionar Pagamento Maquininha (SmartPOS detectado pelo UA mockado)
  const cardBtn = page.getByRole('button', { name: /MAQUININHA/i });
  await expect(cardBtn).toBeVisible();
  await cardBtn.click();

  // 8. Clicar em Pagar
  await page.getByRole('button', { name: /Pagar na Máquina/i }).click();

  // 9. Validar Intent URL (Lendo a variável global injetada)
  const intentUrl = await page.evaluate(() => (window as any).__intentUrl);
  console.log('💳 Intent Gerado:', intentUrl);
  
  expect(intentUrl).toContain('stone://payment');
  expect(intentUrl).toContain('amount=');
  expect(intentUrl).toContain('transaction_type=CREDIT');
});