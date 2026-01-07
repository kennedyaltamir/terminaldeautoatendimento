import { test, expect } from '@playwright/test';

test.describe('Cash Drawer Trigger', () => {
  test('deve gerar link rawbt para abrir gaveta ao pagar em dinheiro', async ({ page, context }) => {
    // 1. Mock do window.location (Estratégia Proxy)
    await page.addInitScript(() => {
      // Cria um proxy para interceptar atribuições ao location
      // Nota: Em alguns browsers, location é readonly/non-configurable.
      // Se falhar, tentamos capturar via evento de clique no link (se fosse um <a>)
      // Mas como é window.location.href = ..., a melhor chance é tentar sobrescrever a propriedade no protótipo ou na instância.
      
      try {
          let _href = window.location.href;
          Object.defineProperty(window, 'location', {
            value: {
                get href() { return _href; },
                set href(val) { 
                    console.log('Navegação interceptada:', val);
                    (window as any).__intentUrl = val; 
                    _href = val;
                },
                assign: (val: string) => {
                    console.log('Assign interceptado:', val);
                    (window as any).__intentUrl = val;
                },
                replace: (val: string) => {
                    console.log('Replace interceptado:', val);
                    (window as any).__intentUrl = val;
                },
                reload: () => {},
                toString: () => _href
            },
            writable: true,
            configurable: true
          });
      } catch (e) {
          console.error("Falha crítica ao mockar location:", e);
      }
    });

    // 2. Mock do User Agent para simular Android (Gatilho do RawBT)
    await context.addInitScript(() => {
      Object.defineProperty(navigator, 'userAgent', {
        value: 'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36',
        configurable: true
      });
    });

    // 3. Setup Auth
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'fake-jwt-token');
      window.localStorage.setItem('mesaflow_user_role', 'cashier');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });

    // 4. Mocks de API
    await page.route('**/api/admin/company/me', async route => {
      await route.fulfill({ status: 200, json: { name: "Bar do Zé", plan_tier: "pro" } });
    });

    await page.route('**/api/hamburgueria-ze/menu', async route => {
      await route.fulfill({ status: 200, json: { 
        company: { name: "Bar do Zé" }, 
        categories: [{ id: 1, name: "Geral", products: [{ id: 1, name: "Item", price: 10.00, option_groups: [] }] }] 
      }});
    });

    await page.route('**/api/admin/hamburgueria-ze/orders', async route => {
      await route.fulfill({ status: 200, json: [] });
    });

    await page.route('**/api/hamburgueria-ze/orders', async route => {
      await route.fulfill({ status: 201, json: { id: 'ord-1' } });
    });

    // 5. Navegar para Balcão
    await page.goto('/admin/hamburgueria-ze/counter', { waitUntil: 'domcontentloaded' });

    // 6. Adicionar Item
    const itemBtn = page.getByText('Item');
    await expect(itemBtn).toBeVisible({ timeout: 10000 });
    await itemBtn.click();

    // 7. Pagar em Dinheiro
    const cashBtn = page.getByText('DINHEIRO');
    await expect(cashBtn).toBeVisible();
    await cashBtn.click();

    // 8. Verificar se o link rawbt foi gerado
    // Aumentamos o timeout e usamos polling para esperar a variável ser definida
    await expect.poll(async () => {
        return await page.evaluate(() => (window as any).__intentUrl);
    }, {
        timeout: 5000,
        message: 'A variável __intentUrl não foi definida a tempo.'
    }).toContain('rawbt:base64,');
  });
});
