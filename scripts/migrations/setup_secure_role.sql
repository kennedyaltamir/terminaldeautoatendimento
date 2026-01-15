# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 01:15:00
-- Cria um usuário de aplicação com privilégios mínimos (Sem BYPASSRLS)
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'mesaflow_app') THEN
    CREATE ROLE mesaflow_app WITH LOGIN PASSWORD 'mesaflow_secure_pass';
  END IF;
END
$$;
-- Garante acesso ao Schema Public
GRANT USAGE ON SCHEMA public TO mesaflow_app;
-- Garante acesso a todas as tabelas atuais
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mesaflow_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mesaflow_app;
-- Garante acesso a tabelas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mesaflow_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO mesaflow_app;

