# 💰 External Reconciliation Protocol (ERP) v2.0
**Versão:** 10.0.1-AUTO | **Domínio:** FINTECH | **Status:** ENFORCED

## 1. Thresholds Críticos de Alerta
| Indicador | Threshold | Ação Automática |
| :--- | :--- | :--- |
| **Divergência de Valor** | > R$ 0,00 | Bloqueio de Saques do Tenant |
| **Transação Ghost** | 1 ocorrência | Suspensão da API Key do Provedor |
| **Transação Orphan** | > 5 ocorrências | Alerta de Fraude / Reconciliação Manual |

## 2. Validação Contínua (Zero-Latency)
O sistema utiliza um **Shadow Ledger** em Redis para validação instantânea:
- Toda entrada no DB é espelhada no Redis.
- O script `FIN-01` compara DB vs Redis a cada 5 minutos.
- Divergência detectada = `CircuitBreaker.OPEN` para o módulo financeiro.

## 3. Sinalização Antecipada
O `ReconciliationService` monitora o status `pending` no Gateway. Se um pagamento ficar `pending` por > 24h sem entrada no Ledger, o sistema cria uma **Task de Investigação** automática no `TASKS.md`.

