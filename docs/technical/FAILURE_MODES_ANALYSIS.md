
# 📄 Failure Modes & Effects Analysis (FMEA) - MesaFlow OS

## 1. Infraestrutura Core

| Componente | Modo de Falha | Impacto | Mitigação / Fallback | Runbook |
| :--- | :--- | :--- | :--- | :--- |
| **Database (Neon)** | Indisponibilidade | Parada de escrita. | Modo Read-Only via cache. | [RB-001](#rb-001) |
| **Redis (Pub/Sub)** | Queda do serviço | Perda de Real-time. | Fallback para HTTP Polling. | [RB-002](#rb-002) |
| **API Gateway** | SLO Breach (Latência) | Lentidão sistêmica. | Abertura do Circuit Breaker. | [RB-003](#rb-003) |

## 2. Domínio Transacional

| Cenário | Risco | Resolução Determinística | Runbook |
| :--- | :--- | :--- | :--- |
| **Double Spend** | Cobrança Duplicada | Idempotency Key Check. | [RB-004](#rb-004) |
| **Sync Conflict** | Pedido em Mesa Fechada | Rejeição por Estado Terminal. | [RB-005](#rb-005) |

---
**Status:** Ativo | **Referência:** docs/sre/RUNBOOKS.md

