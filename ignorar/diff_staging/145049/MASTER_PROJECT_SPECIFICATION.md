# DOMAIN: ROOT_CONFIG
# LAST_MODIFIED: 2026-01-15 14:50:00
# 📘 MASTER PROJECT SPECIFICATION — MesaFlow OS
**Caminho Físico:** `/MASTER_PROJECT_SPECIFICATION.md`  
**Versão:** 5.0 — Gold Master Sealed  
**Status de Prontidão:** `GOLD_MASTER_SEALED`  
**Classificação:** Confidencial  
**Autoridade:** Fonte Única de Verdade (SSOT)
---
## 1. Contexto, Missão e Visão
O **MesaFlow OS** é uma infraestrutura operacional de missão crítica para ambientes de alta rotatividade. O sistema elimina a fricção entre o desejo do cliente e a entrega do serviço através de uma orquestração digital resiliente e auditável.
---
## 2. Arquitetura Geral do Sistema
O MesaFlow adota o padrão **Monólito Modular Híbrido**, priorizando consistência transacional e isolamento multi-tenant via banco de dados.
### 2.1 Stack Tecnológica Oficial
| Camada | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Backend** | Python 3.11 + FastAPI | Orquestração e APIs determinísticas |
| **Frontend Web** | Next.js 14 (App Router) | Admin, Dashboards e PWA Cliente |
| **Mobile** | React Native (Expo SDK 52) | Super App Operacional (Staff/KDS/Logística) |
| **Persistência** | PostgreSQL 15 (Neon) | Dados relacionais com isolamento RLS |
| **Eventos** | Redis Pub/Sub + WebSockets | Sincronização instantânea multi-persona |
---
## 3. Segurança e Isolamento (L6 Standard)
- **PostgreSQL RLS:** Isolamento físico de dados por Tenant em nível de engine.
- **Financial Ledger:** Cadeia de custódia imutável com encadeamento de hashes.
- **Idempotência:** Proteção contra duplicidade em todas as transações críticas.
---
## 4. Estados de Prontidão (Registry)
### 🟢 HOMOLOGADOS (RELEASE READY)
- **SYS-01:** Integridade Estrutural Validada.
- **SEC-01:** Isolamento RLS Blindado.
- **FIN-01:** Ledger Financeiro Íntegro.
- **QA-05:** Automação L8.8 (Full Loop) Aprovada.
- **OBS-01:** Telemetria Sentry Ativa.
---
## 5. Declaração Final
O **MesaFlow OS** é declarado **Estável, Seguro e Escalável**. Esta versão constitui a baseline definitiva para o lançamento comercial.
**MesaFlow Technology — Engineered for Stability, Sealed for Market.**
