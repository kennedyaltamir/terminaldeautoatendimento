# 📱 Task 29C: Revisão e Envio de Pedido (Checkout)

## 1. Contexto
Finalização do fluxo de atendimento nativo. Esta missão implementa a tela de revisão do carrinho e a integração com o backend para persistência do pedido, garantindo que o garçom possa concluir a venda de forma segura e rápida.

## 2. Decisões Técnicas
- **Order Submission Logic:** A `WaiterStore` agora encapsula a chamada de API. Utilizamos o `api.ts` (Axios) para garantir que o token JWT e o tratamento de refresh sejam aplicados automaticamente.
- **Checkout UI:** Criada a `OrderReviewScreen` com foco em clareza financeira. O total é exibido em destaque e o botão de envio possui estado de carregamento integrado.
- **Post-Submission Flow:** Após o sucesso, o estado do garçom é resetado (`resetWaiterFlow`) e a navegação retorna para a raiz (`WaiterTables`), preparando o dispositivo para o próximo atendimento.
- **Error Resilience:** Implementado tratamento de erro com `Alert` nativo para falhas de rede ou validação de backend, impedindo a perda do carrinho em caso de erro temporário.

## 3. Arquivos Afetados
- `mobile/src/store/waiter.store.ts` (Lógica de envio)
- `mobile/src/screens/waiter/OrderEntryScreen.tsx` (Navegação para revisão)
- `mobile/src/screens/waiter/OrderReviewScreen.tsx` (Nova interface)
- `mobile/src/navigation/stacks/AppStack.tsx` (Registro de rota)

## 4. Próximos Passos
**Missão 30:** Integração com Impressão Bluetooth Nativa para emissão de tickets de conferência diretamente do Mobile POS.

---
*Fase 11 — Janeiro de 2026*
