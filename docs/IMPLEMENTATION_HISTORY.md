# 📜 Histórico de Implementação e Desafios Superados

## 1. Sincronização de Estado e Race Conditions (Frontend)
**Desafio:** Durante os testes E2E, o robô era mais rápido que a renderização do React. Ao remover um item do carrinho, o teste falhava porque o elemento ainda constava no DOM por alguns milissegundos.
**Solução:** Implementamos o uso de `wait_for_function` no Playwright e `useEffect` com dependências estritas no React. Aprendemos que em SPAs complexas, a validação deve ser baseada em **estado final** e não em tempo fixo.

## 2. Integridade Financeira (Decimal vs Float)
**Desafio:** Erros de centavos acumulados em pedidos grandes com muitos adicionais.
**Solução:** Refatoração completa de `float` para `Decimal` no Backend e Schemas. No Frontend, os cálculos são feitos em ponto flutuante mas formatados via `Intl.NumberFormat` apenas na exibição, com validação final sempre no servidor.

## 3. Resiliência Fiscal (Store & Forward)
**Desafio:** Restaurantes perdiam vendas ou operavam ilegalmente quando a internet caía, pois não conseguiam emitir NFC-e.
**Solução:** Criamos uma arquitetura de contingência usando `Dexie.js` (IndexedDB). A nota é "emitida" localmente (salva na fila) e o hook `useFiscalSync` realiza a transmissão automática assim que o evento `online` é detectado pelo navegador.

## 4. Middleware iFood (Mapeamento Polimórfico)
**Desafio:** Injetar pedidos de uma API externa (iFood) em um sistema multi-tenant sem duplicar dados ou perder a referência de produtos.
**Solução:** Implementamos um serviço de polling assíncrono que utiliza o `external_order_id` como chave de idempotência. O mapeamento de produtos é feito via `external_id` (SKU) com um join dinâmico entre `Product` e `Category` para garantir o isolamento do tenant.

---
*Este diário serve como base para evitar a repetição de erros passados.*
# 📜 Diário de Engenharia: Desafios e Soluções

## 1. O Problema das Race Conditions no Frontend
**Cenário:** Em conexões lentas, o usuário clicava duas vezes no botão "Adicionar" antes do modal fechar.
**Solução:** Implementamos **Atualizações Otimistas** e bloqueio de UI (Loading States) via React Hook Form. Nos testes E2E, passamos a usar `expect(locator).toBeVisible()` com timeouts dinâmicos para respeitar o tempo de renderização do Next.js.

## 2. Por que Polling para o iFood?
**Decisão:** O iFood oferece Webhooks, mas optamos por **Polling de 30s** como primário.
**Racional:** Webhooks podem ser perdidos se o nosso servidor oscilar. O Polling garante que buscaremos todos os eventos acumulados na fila do iFood, tratando a ingestão de forma sequencial e segura (Idempotência via `external_order_id`).

## 3. Sincronização de Estoque (Regra 86)
**Desafio:** Evitar a venda de um produto cujo ingrediente acabou de zerar em outra mesa.
**Solução:** Implementamos um **Trigger de Banco de Dados** (SQL) combinado com **WebSockets**. Assim que o `current_stock` atinge 0, o backend dispara um broadcast `product_update` que desativa o botão de compra em todos os celulares conectados instantaneamente.

## 4. Compatibilidade SQLite/Postgres
**Desafio:** Rodar testes rápidos em SQLite e produção em Postgres.
**Solução:** Criamos o tipo customizado `GUID` em `app/models.py`. Ele detecta o dialeto do banco: se for Postgres, usa o tipo `UUID` nativo; se for SQLite, usa `CHAR(36)` e gerencia a conversão de strings para objetos UUID automaticamente.

---
