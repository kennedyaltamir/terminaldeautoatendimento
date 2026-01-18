# 🛡️ Runtime RLS Guard: Blindagem de Scripts e Dashboards
**Versão:** 10.0.1-AUTO | **Domínio:** SECURITY | **Status:** ACTIVE

## 1. Mitigação de Queries Administrativas
Queries que operam fora do RLS (Superuser/Admin) devem utilizar o wrapper `AdminContext`:
- **Regra:** O uso de `AdminContext` dispara obrigatoriamente um `AuditLog` de nível `CRITICAL`.
- **Bloqueio:** Scripts de manutenção (`scripts/maintenance/*`) são impedidos de conectar ao banco sem um `company_id` definido, a menos que possuam a flag `BYPASS_RLS_AUTHORIZED`.

## 2. Dashboard de Violação SRE
Métricas exportadas para o Prometheus/Grafana:
- `rls_denied_queries_per_minute`: Picos indicam tentativa de invasão ou bug de contexto.
- `missing_tenant_context_total`: Contador de falhas no middleware de injeção.
- `unauthorized_admin_access_attempts`: Tentativas de uso do `AdminContext` sem permissão.

## 3. Alertas Proativos
- **Severity HIGH:** > 5 violações de RLS em 1 minuto para o mesmo IP.
- **Severity CRITICAL:** Qualquer falha de `set_tenant` em rotas de `/api/admin/*`.

