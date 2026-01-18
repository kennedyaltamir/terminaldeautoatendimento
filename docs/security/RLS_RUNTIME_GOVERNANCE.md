# 🛡️ RLS Runtime Governance L10.2: Bloqueio e Auto-Correção
**Versão:** 10.0.2-AUTO | **Domínio:** SECURITY | **Status:** ACTIVE

## 1. Bloqueio de Scripts e Dashboards sem Contexto
- **Mecanismo:** Introdução de um `TenantContextGuard` no `get_db` do `database.py`.
- **Regra:** Se a role da sessão for `mesaflow_app` e a variável `app.current_company_id` for nula, a conexão com o banco de dados é **recusada** com um `HTTP 500: Tenant Context Missing`.
- **Scripts de Manutenção:** Scripts que precisam de acesso global devem ser executados com um usuário administrativo (`postgres`) e declarar a flag `--allow-cross-tenant` para registrar a auditoria.

## 2. Alertas e Self-Healing para Falhas de `set_tenant`
- **Alerta Sentry:** Toda falha no `try/except` do `set_tenant` agora gera um alerta no Sentry com `severity: fatal` e a tag `context_leak_attempt`.
- **Self-Healing:** O `Circuit Breaker` é configurado para abrir para o IP do cliente que causou a falha de contexto por 60 segundos, bloqueando novas tentativas.

## 3. Auditoria de Queries Administrativas com Shadow Logging
- **Mecanismo:** Uma trigger no PostgreSQL replica todas as queries executadas pelo usuário `postgres` para uma tabela `admin_query_log` particionada por data.
- **Performance:** A trigger opera de forma assíncrona, garantindo **zero impacto** na performance das queries originais.
- **Análise:** Um script semanal (`scripts/security/analyze_admin_logs.py`) varre os logs em busca de `SELECT *` em tabelas com mais de 1M de registros ou `UPDATE/DELETE` sem `WHERE`.

