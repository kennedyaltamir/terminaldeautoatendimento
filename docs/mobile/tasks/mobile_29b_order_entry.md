# 📱 Task 29B: Lançamento de Itens (Order Entry)

## 1. Contexto
Implementação da funcionalidade core do Mobile POS: a capacidade de lançar itens em uma comanda. Esta missão conecta a seleção de mesas à navegação no cardápio e gestão de um carrinho de compras nativo.

## 2. Decisões Técnicas
- **Volatile Cart:** O carrinho reside na `WaiterStore` e é limpo ao resetar o fluxo. Isso garante que o garçom não carregue itens de uma mesa para outra por engano.
- **Search & Filter:** Implementada busca local (client-side) sobre a lista de produtos da categoria ativa para garantir resposta instantânea ao digitar.
- **Counter Logic:** O componente de produto alterna entre "Adicionar" e um "Contador" (+/-) caso o item já esteja no carrinho, mimetizando o comportamento de apps de delivery modernos.
- **Navigation Guard:** A tela de lançamento exige um `selectedTableId`. Caso o estado seja perdido, o garçom é redirecionado para o mapa de mesas.

## 3. Arquivos Afetados
- `mobile/src/store/waiter.store.ts` (Lógica de carrinho)
- `mobile/src/screens/waiter/WaiterTablesScreen.tsx` (Navegação)
- `mobile/src/screens/waiter/OrderEntryScreen.tsx` (Nova interface)
- `mobile/src/navigation/stacks/AppStack.tsx` (Registro de rota)

## 4. Próximos Passos
**Missão 29C:** Revisão do pedido (Checkout) e envio para o backend com integração de WebSockets para confirmação.

---
*Fase 11 — Janeiro de 2026*
