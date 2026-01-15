
# LOG DE AÇÃO: DIAGNÓSTICO RLS
**Data:** 12/01/2026
**Executor:** Kernel-INDA
**Task:** DIAGNOSTIC-RLS

## 1. Ação Realizada
Criação do script `scripts/diagnostics/inspect_rls_context.py` para investigar a falha de isolamento detectada no incidente INC-SEC-20260112-002.

## 2. Detalhes Técnicos
- **Objetivo:** Verificar se o RLS está habilitado no banco e se a variável de sessão `app.current_company_id` está sendo propagada corretamente pelo SQLAlchemy.
- **Método:** Queries diretas nas tabelas de sistema do PostgreSQL (`pg_class`, `pg_policy`) e teste de `current_setting`.
- **Segurança:** Read-only (exceto pelo `set_tenant` na sessão temporária).

## 3. Status
- Script criado: ✅
- Registry atualizado: ✅
- Relatório de Incidente criado: ✅

