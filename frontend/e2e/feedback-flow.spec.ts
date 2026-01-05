import { test, expect } from '@playwright/test';

test.describe('Order Feedback Flow', () => {
  test('deve permitir avaliar um pedido finalizado', async ({ page }) => {
    // 1. Mock da API de Pedido (Simulando entregue e pago)
    await page.route('**/api/orders/order-123', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 'order-123',
          status: 'delivered',
          payment_status: 'paid',
          total_amount: 50.00,
          items: [{ quantity: 1, product: { name: 'X-Bacon', price: 50.00 }, selected_options: [] }],
          feedback: null,
          company: { slug: 'hamburgueria-ze', name: 'Hamburgueria Zé' },
          created_at: new Date().toISOString(),
          payment_method: 'online',
          order_type: 'delivery'
        })
      });
    });

    // 2. Mock do Envio de Feedback
    await page.route('**/api/hamburgueria-ze/orders/order-123/feedback', async (route) => {
      await route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({ message: "Obrigado!" })
      });
    });

    // 3. Injetar estado de pedido ativo
    await page.addInitScript(() => {
      localStorage.setItem('mesaflow_active_order', 'order-123');
    });

    // 4. Navegar para a página
    await page.goto('/hamburgueria-ze/menu');

    // 5. Aguardar o gatilho automático (2s no código + 1s de margem)
    await page.waitForTimeout(3500);

    // 6. Verificar se o modal abriu ou clicar no botão manual
    const modalTitle = page.getByText('Como foi sua experiência?');
    const isModalVisible = await modalTitle.isVisible();

    if (!isModalVisible) {
      // Se o modal automático falhar, tentamos o botão manual com scroll
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      const btn = page.getByTestId('btn-avaliar');
      await expect(btn).toBeVisible();
      await btn.click();
    }

    // 7. Preencher avaliação
    await expect(page.getByText('Como foi sua experiência?')).toBeVisible();
    
    // Clicar na 5ª estrela (A última do container de estrelas)
    await page.locator('.flex.justify-center.gap-2 button').last().click();

    // Escrever comentário
    await page.getByPlaceholder('Deixe um comentário').fill('Atendimento nota 10!');

    // 8. Enviar
    await page.getByText('Enviar Avaliação').click();

    // 9. Verificar Mensagem de Sucesso Final
    await expect(page.getByText('Obrigado!')).toBeVisible();
  });
});
