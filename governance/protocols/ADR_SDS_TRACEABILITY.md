# 🔗 Matriz de Rastreabilidade: ADR -> SDS -> TASK
**Versão:** 5.0.2-SEQ | **Domínio:** GOVERNANCE

| ADR ID | Decisão Técnica | SDS Relacionado | Task de Implementação |
| :--- | :--- | :--- | :--- |
| **ADR-001** | PostgreSQL RLS para Multi-tenancy | `BACKEND_SDS.md` | `TASK-SEC-01` |
| **ADR-002** | Ledger L7 com Hash Chain | `BACKEND_SDS.md` | `TASK-FIN-01` |
| **ADR-003** | Dexie.js para Offline-First | `FRONTEND_SDS.md` | `TASK-MOB-01` |
| **ADR-004** | Event Adapter para WebSockets | `BACKEND_SDS.md` | `QA-05` |

## 1. Decisões sem Rastreabilidade (Backlog)
- Escolha do Redis como Broker de WebSocket (Implícito, falta ADR formal).
- Uso de NativeWind no Mobile (Implícito, falta ADR formal).