
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 12:20:00
# 🚨 RELATÓRIO DE INCIDENTE: VAZAMENTO MULTI-TENANT (RLS)
**Data:** 13/01/2026
**Severidade:** CRÍTICA (BLOCKER)
**Status:** EM REMEDIAÇÃO

## 1. Falha Detectada
Durante a execução do script `verify_TASK-SEC-01.py`, o sistema permitiu que um contexto de banco de dados (Tenant B) visualizasse dados privados de outro contexto (Tenant A).

## 2. Causa Raiz
As tabelas no PostgreSQL não possuíam a flag `FORCE ROW LEVEL SECURITY`. Em ambientes de desenvolvimento/Docker, a aplicação costuma conectar com usuários de alta permissão (ex: `postgres`), que ignoram o RLS por padrão a menos que o `FORCE` seja aplicado explicitamente.

## 3. Ação Corretiva
1.  **Registry Lock:** O sistema foi marcado como `FAILED` no `registry.xml` para impedir deploys.
2.  **Hardening Script:** Criado o `scripts/validar/apply_rls_hardening.py` para forçar a segurança em todas as 14 tabelas transacionais.

## 4. Re-validação Necessária
O sistema só será considerado seguro após o `verify_TASK-SEC-01.py` retornar `✅ PASS`.

