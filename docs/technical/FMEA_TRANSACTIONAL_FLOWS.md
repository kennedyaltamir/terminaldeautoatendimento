# 🚨 Failure Mode and Effects Analysis (FMEA): Fluxos Transacionais
**Versão:** 5.0.2-SEQ | **Domínio:** SRE | **Status:** ENFORCED

## 1. Matriz de Riscos e Mitigações
| Fluxo | Modo de Falha | Impacto | Mitigação (L8/L9) | Mecanismo de Rollback |
| :--- | :--- | :--- | :--- | :--- |
| **Criação de Pedido** | Deadlock em `order_items` | Timeout da API | `select_for_update(skip_locked=True)` | `SimulationTransaction` cancela via ID |
| **Pagamento (MP)** | Webhook duplicado (Race) | Double Credit no Ledger | Idempotência via `UniqueConstraint(provider, external_id)` | Rejeição silenciosa (200 OK) |
| **Despacho (Driver)** | Falha de rede pós-coleta | Pedido "preso" em Delivering | Heartbeat de GPS; se > 5min sem sinal, alerta SRE | Reversão manual via Manager POS |
| **Ledger L7** | Sequence Gap (Identity fail) | Quebra da cadeia de hash | `db.flush()` forçado antes do cálculo do hash | Suspensão de transações do Tenant |

## 2. Melhorias no SimulationTransaction (L8+)
- **Multi-tenant Isolation:** O cleanup agora verifica o `owner_id` do pedido antes de disparar o cancelamento, impedindo que uma falha no script de teste afete pedidos reais de outros tenants.
- **Atomic State Recovery:** Implementação de `SAVEPOINT` no PostgreSQL para permitir rollback parcial de itens sem perder o log de erro da transação principal.

