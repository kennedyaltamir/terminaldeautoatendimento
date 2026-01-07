# 📱 Task 29A: Fundação do Mobile POS & Gestão de Mesas

## 1. Contexto
Início da transição das funcionalidades de atendimento do PWA para o App Nativo. Esta missão foca na infraestrutura de estado e na interface de seleção de mesas, permitindo que o garçom visualize o status do salão em tempo real.

## 2. Decisões Técnicas
- **Waiter Store:** Criada para gerenciar o contexto de atendimento. O estado é volátil (não persistido), pois a seleção de mesa deve ser reiniciada a cada sessão de uso para evitar erros de lançamento.
- **Role-Based Routing:** A `AppStack` agora decide a tela inicial baseada no cargo do usuário. Funcionários de `kitchen` caem no KDS; `owner`, `manager` e `cashier` caem no mapa de mesas.
- **UI Composition:** A `WaiterTablesScreen` utiliza um grid de 2 colunas para maximizar a densidade de informação em telas de smartphone.
- **Realtime Integration:** Embora a tela de mesas use fetch (HTTP), ela é notificada via WebSocket (através da `OrdersStore`) para disparar re-fetchs quando pedidos são alterados, garantindo sincronia visual.

## 3. Arquivos Afetados
- `mobile/src/store/waiter.store.ts` (Novo)
- `mobile/src/screens/waiter/WaiterTablesScreen.tsx` (Novo)
- `mobile/src/navigation/stacks/AppStack.tsx` (Roteamento)

## 4. Próximos Passos
**Missão 29B:** Implementação da tela de lançamento de itens (Order Entry) e integração com o carrinho nativo.

---
*Fase 11 — Janeiro de 2026*
