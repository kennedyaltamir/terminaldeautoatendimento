# 🚨 FMEA Avançado: Modos de Falha Residual e Rollback em Cascata
**Versão:** 10.0.1-AUTO | **Domínio:** SRE | **Status:** ENFORCED

## 1. Modos de Falha Residual (Multi-tenant)
| Modo de Falha | Causa Raiz | Impacto | Mitigação L10 |
| :--- | :--- | :--- | :--- |
| **Partial Task Success** | Webhook enviado mas Ledger falhou | Inconsistência entre Gateway e DB | Task de compensação atômica (Saga Pattern) |
| **Tenant Resource Starvation** | Query pesada de um Tenant bloqueia o DB | Latência global (Cross-tenant impact) | Statement Timeout granular por Tenant Role |
| **Orphan Ledger Entry** | Sequence ID gerado mas transação abortada | Buraco na cadeia de auditoria | Auditoria de Gaps de Sequência (FIN-02) |

## 2. SimulationTransaction L10 (Cascading Rollback)
O mecanismo agora suporta a reversão de efeitos colaterais em serviços externos:
- **Hook de Reversão:** Se o banco sofrer rollback, o `SimulationTransaction` dispara um sinal para o `WebhookDispatcher` invalidar payloads já enfileirados.
- **State Locking:** Durante a simulação, o registro do pedido é marcado como `is_test: true`, impedindo que tasks de produção (ex: faturamento real) o processem.

