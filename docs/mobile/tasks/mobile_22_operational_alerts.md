# 📱 Task 22: Alertas Operacionais & Atenção do Operador (Refactor)

## 1. Contexto
Implementação da camada de "Atenção Ativa" no KDS Mobile. O sistema interrompe o operador em momentos de criticidade temporal (SLA).

## 2. Hardening Arquitetural (v2.0)
- **Engine Pura**: A `AlertsEngineService` agora é uma camada de decisão sem side-effects. Ela recebe a lista de pedidos e retorna `AlertDecision[]`.
- **Injeção de Tempo**: Removido o uso de `Date.now()` nos serviços. O tempo flui do `GlobalClock` -> `AppStack` -> `Store` -> `Services`.
- **Store como Orquestradora**: A `OrdersStore` assumiu a responsabilidade de executar os alertas físicos (via `AlertsOutputService`) e gerenciar o histórico de interrupções (`lastAlertedAt`).
- **Navegação Limpa**: O `AppStack` foi simplificado para atuar apenas como disparador de pulso, delegando a lógica de negócio para a Store.

## 3. Matriz de Alertas
- **CRITICAL**: Vibração curta única. Ativado na transição de estado.
- **BREACHED**: Vibração dupla intensa. Ativado na entrada e recorrentemente a cada 60s (Cooldown).

---
*Fase 10 — Janeiro de 2026*
