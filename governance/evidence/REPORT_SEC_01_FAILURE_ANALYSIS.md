
# 🛡️ Análise de Falha Crítica: SEC-01 (RLS Leak)

**Incidente:** O Tenant B acessou dados do Tenant A durante o MRC.
**Causa:** No PostgreSQL, políticas de RLS são ignoradas por Superusers. O ambiente de desenvolvimento/CI está operando com o usuário `postgres`.
**Ação Corretiva:** 
1. Criar Role `mesaflow_app` sem privilégios de superuser.
2. Alterar `app/database.py` para garantir que o pool de conexões execute `SET row_security = on`.
3. Forçar `ALTER TABLE ... FORCE ROW LEVEL SECURITY`.

