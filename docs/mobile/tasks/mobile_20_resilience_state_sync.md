# 📱 Task 20: Resiliência de Conectividade & State Sync

## 1. Objetivo
Garantir a continuidade da operação do KDS Mobile em ambientes de rede instáveis, implementando recuperação automática de conexão e consistência de dados em tempo real.

## 2. Estratégia de Resiliência (v1.0)
- **Exponential Backoff:** O aplicativo não tenta reconectar loucamente. O intervalo entre tentativas cresce (2s, 4s, 8s...) até o limite de 30s.
- **State Reconciliation:** Ao reconectar, o app ignora o estado local e realiza um `performFullSync`. Isso garante que pedidos criados ou alterados durante o período offline sejam sincronizados corretamente.
- **Optimistic UI:** O avanço de status no KDS é instantâneo na interface. A Store gerencia o rollback caso a API falhe, eliminando a sensação de "travamento" para o operador.

## 3. Resolvendo Gaps Legados
- **Full new_order:** Ao receber o evento de novo pedido, o `OrdersSyncService` busca o objeto completo no backend, permitindo que novos pedidos apareçam na tela sem necessidade de re-fetch manual.

## 4. Definição de Conectividade
A resiliência é tratada em nível de **Infraestrutura Invisível**. A UI não possui indicadores de erro de conexão, delegando a responsabilidade total para os Services e Stores.

---
*Fase 10 — Janeiro de 2026*
