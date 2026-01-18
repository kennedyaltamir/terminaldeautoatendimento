# 🛡️ RLS & Compliance Hardening: Runtime Guard
**Versão:** 5.0.2-SEQ | **Domínio:** SECURITY | **Status:** ACTIVE

## 1. Detecção de Vazamento de Contexto (Pre-flight)
Para garantir que `set_tenant` foi aplicado, o sistema implementa um **Assert de Sessão** em nível de driver:
- **Regra:** Toda query disparada por `mesaflow_app` que não contenha a variável `app.current_company_id` definida resulta em `ERROR: 42P17 (Check violation)`.

## 2. Queries Críticas para Monitoramento
As seguintes operações ignoram o RLS (Admin Only) e devem ser auditadas via Sentry/CloudWatch:
- `SELECT * FROM companies` (Global Discovery)
- `SELECT sum(amount) FROM financial_ledger` (Global Billing)
- `UPDATE feature_flags` (Support Impersonation)

## 3. Métricas SRE em Tempo Real
- `rls_violation_attempts_total`: Contador de queries bloqueadas pelo Postgres.
- `tenant_context_latency_ms`: Tempo gasto na injeção de contexto via middleware.
- `cross_tenant_query_count`: Alerta crítico se uma query administrativa tocar em mais de 10 tenants simultaneamente.

