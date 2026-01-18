# 🚨 FMEA L10.2: Riscos Residuais e Mitigação Autônoma
**Versão:** 10.0.2-AUTO | **Domínio:** SRE | **Status:** ENFORCED

## 1. Modos de Falha em Tasks Assíncronas Multi-Tenant
| Modo de Falha | Causa Raiz | Impacto | Mitigação Autônoma L10.2 |
| :--- | :--- | :--- | :--- |
| **Deadlock de Recurso** | Task A (Tenant 1) bloqueia a tabela `products` enquanto a Task B (Tenant 2) aguarda | Atraso em cascata em todas as filas | **Preemption:** O worker Celery detecta `LockTimeout` e move a Task B para uma fila de baixa prioridade, liberando o worker. |
| **Falha de Webhook Externo** | API do parceiro (ex: iFood) retorna `503 Service Unavailable` | Retry Storm esgota a cota de API e workers | **Backoff Adaptativo com Circuit Breaker:** Se a taxa de erro > 50%, o `dispatch_webhook_task` entra em modo de suspensão por 5 min para aquele endpoint. |
| **Rollback Parcial** | Pedido criado no DB, mas falha ao enfileirar notificação no Redis | Cliente não recebe notificação de "Pedido Recebido" | **Saga Pattern:** O `OrderService` dispara uma `task de compensação` que cancela o pedido se a task de notificação falhar 3 vezes. |

## 2. Automação de Correção de Inconsistências Externas
O `SimulationTransaction` foi estendido para incluir **Hooks de Compensação**:
- `on_failure_post_commit`: Se uma falha ocorrer após o commit do DB (ex: erro no Redis), o hook dispara uma task Celery com `priority: CRITICAL` para reverter o estado ou alertar o SRE.
- **Cache Invalidation:** O `SimulationTransaction` agora registra as chaves de cache que seriam escritas. Em caso de rollback, ele dispara um `DELETE` para essas chaves no Redis.

## 3. Métricas de SRE para Rollback em Cascata
- `sre_saga_compensation_triggered_total`: Contador de eventos de compensação.
- `sre_rollback_external_latency_ms`: Tempo gasto para reverter efeitos em APIs externas.
- `sre_partial_failure_rate`: % de transações que exigiram compensação.

