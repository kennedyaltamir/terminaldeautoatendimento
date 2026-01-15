# 🔎 RLS Policy Inventory Report (SEC-01A)

## Objetivo
Validar o estado do Row-Level Security nas tabelas core de negócio.

## Evidência Forense (pg_catalog)
| Tabela | RLS | Force | Política | Comando | Expressão USING |
| :--- | :---: | :---: | :--- | :---: | :--- |
| orders | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| companies | ✅ | ✅ | tenant_isolation_policy | * | `(id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| employees | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| products | ✅ | ✅ | tenant_isolation_policy | * | `(category_id IN ( SELECT categories.id
   FROM categories
  WHERE (categories.company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)))` |
| categories | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| tables | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| table_sessions | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| financial_ledger | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| ingredients | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |
| promotions | ✅ | ✅ | tenant_isolation_policy | * | `(company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)` |


## Veredito Técnico
✅ **PASS:** Todas as tabelas core auditáveis possuem RLS habilitado.
