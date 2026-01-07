# 📱 Task 17: Módulo de Pedidos (KDS Nativo)

## 1. Objetivo
Implementação da primeira funcionalidade operacional nativa. O foco é a listagem e progressão de pedidos ativos, validando o consumo de APIs protegidas pelo fluxo de autenticação semântica.

## 2. Decisões de Arquitetura
- **Unidirectional Data Flow**: A UI dispara ações na `OrdersStore`, que consome o `OrdersService`. O estado é atualizado apenas após a confirmação do backend.
- **Refetch Strategy**: Para simplificar a primeira versão, optamos por um re-fetch total da lista após cada atualização de status, garantindo que o estado da tela esteja sempre sincronizado com o banco de dados.
- **UI Compliance**: Cards e botões utilizam estritamente os componentes da UI Foundation.

## 3. Dívida Técnica (Out of Scope)
- **Slug Injection**: O `company_slug` está fixo como string. Deve ser injetado via Store de Perfil em missões futuras.
- **Real-time**: A atualização automática via WebSockets não faz parte desta entrega.
- **Optimistic UI**: A alteração visual imediata antes da resposta do servidor será implementada em fases de polimento de UX.

---
*Fase 10 — Janeiro de 2026*
# 📱 Task 17: Módulo de Pedidos (KDS Nativo) - Refinado

## 1. Objetivo
Implementação da primeira funcionalidade operacional nativa para gestão de produção.

## 2. Refinamentos Pós-Auditoria
- **Clean UI Logic:** Extração da lógica de tempo decorrido para `src/utils/time.ts`.
- **Token Compliance:** Expansão dos tokens de design para eliminar números brutos no `StyleSheet`.
  - Introduzido `spacing.xxs` para badges.
  - Introduzido `typography.size.xxs` para legendas técnicas.
- **Architectural Debt Record:** Identificado o acoplamento do fluxo de status (`nextStatusMap`) na Store. Esta lógica deve ser delegada ao Backend em versões futuras do contrato de API.

## 3. Comportamento Validado
- [x] Listagem via fetch seguro (JWT).
- [x] Cálculo de tempo reativo ao carregamento.
- [x] Atualização de status com sincronização de lista (Re-fetch).

---
*Fase 10 — Janeiro de 2026*
