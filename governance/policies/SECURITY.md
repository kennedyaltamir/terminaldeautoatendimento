
# 🛡️ Política de Segurança (L6 Enforcement)

## 1. Isolamento de Dados
- Toda tabela multi-tenant **DEVE** possuir RLS (Row-Level Security) ativo.
- O isolamento é garantido via `app.current_company_id` na sessão do Postgres.

## 2. Gestão de Segredos
- É terminantemente proibido o commit de arquivos `.env`.
- Chaves de produção devem ser injetadas via Vault ou Secrets Management do provedor Cloud.

## 3. Controle de Acesso (RBAC)
- O sistema opera sob o princípio do menor privilégio.
- A role `mesaflow_app` não possui permissões de superuser ou bypass de RLS.

