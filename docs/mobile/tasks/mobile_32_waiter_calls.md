# 📱 Task 32: Gestão de Chamados (Waiter Call)

## 1. Contexto
Implementação da funcionalidade de atendimento reativo. O garçom agora pode visualizar e gerenciar solicitações de serviço (ajuda, conta, limpeza) feitas pelos clientes via QR Code, integrando o fluxo de salão ao sistema de tempo real.

## 2. Decisões Técnicas
- **Realtime Routing:** O `AppStack` foi atualizado para interceptar eventos do tipo `waiter_call` e roteá-los para a `WaiterStore`.
- **Visual Urgency:** A `WaiterTablesScreen` agora monitora a lista de chamados. Se uma mesa tiver um chamado pendente, o card assume o estado `alert` (borda vermelha e ícone de sino), priorizando a atenção do garçom.
- **Call Management:** Criada a `WaiterCallsScreen` como um hub central de solicitações, permitindo a resolução atômica de cada chamado.
- **Idempotência de Estado:** A `WaiterStore` verifica a existência do ID do chamado antes de adicioná-lo, prevenindo duplicidade entre o fetch inicial e eventos de WebSocket.

## 3. Arquivos Afetados
- `mobile/src/store/waiter.store.ts` (Lógica de chamados)
- `mobile/src/screens/waiter/WaiterTablesScreen.tsx` (Alertas visuais)
- `mobile/src/screens/waiter/WaiterCallsScreen.tsx` (Nova interface)
- `mobile/src/navigation/stacks/AppStack.tsx` (Roteamento de eventos)

## 4. Próximos Passos
**Missão 33:** Pagamentos e QR Code Nativo — Exibição de Pix dinâmico para recebimento na mesa.

---
*Fase 11 — Janeiro de 2026*
