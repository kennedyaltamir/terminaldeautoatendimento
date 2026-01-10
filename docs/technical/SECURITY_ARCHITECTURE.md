# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 10:30:00
# 🛡️ Arquitetura de Segurança & Multi-tenancy

## 1. Isolamento de Dados (Multi-tenancy)

O MesaFlow utiliza **Isolamento Lógico em Nível de Linha (Row-Level Security - RLS)** nativo do PostgreSQL.

### 1.1 Mecanismo de RLS (PostgreSQL)
Diferente da versão anterior que dependia de filtros `.filter()` no SQLAlchemy, a segurança agora é aplicada pelo motor do banco de dados.

- **Variável de Sessão:** A cada requisição, o backend define `SET LOCAL app.current_company_id = 'UUID'`.
- **Policy de Banco:** Todas as tabelas críticas possuem a seguinte política:
  ```sql
  CREATE POLICY tenant_isolation_policy ON table_name
  USING (company_id = nullif(current_setting('app.current_company_id', true), '')::uuid)
  WITH CHECK (company_id = nullif(current_setting('app.current_company_id', true), '')::uuid)
  ```
- **Fail-Secure:** Se a variável de sessão não estiver definida (ex: erro no código, acesso direto), o banco retorna **zero linhas** ou bloqueia a inserção.

### 1.2 Prevenção de IDOR
Mesmo que um atacante tente acessar `/api/orders/{ID_DE_OUTRO_TENANT}`, o banco de dados se comportará como se aquele registro não existisse, retornando `404 Not Found` em vez de `403 Forbidden` (evitando enumeração).

## 2. Autenticação & Autorização
- **JWT (JSON Web Token):** Utilizado para persistência de sessão. O payload contém `sub` (email), `role`, `account_type` e `company_id`.
- **RBAC (Role Based Access Control):**
    - `owner`: Acesso total, incluindo faturamento e equipe.
    - `manager`: Gestão operacional e cardápio.
    - `cashier`: Operação de mesas e fechamento.
    - `kitchen`: Apenas visualização e avanço de status no KDS.
    - `driver`: Acesso restrito ao módulo de entregas.

## 3. Proteção de Perímetro
- **Rate Limiting:** Implementado via `SlowAPI`. Limites rígidos no login (5/min) e criação de pedidos (10/min por IP).
- **Sanitização:** Todos os inputs de texto passam por `sanitize_html` para prevenir XSS Stored.
- **Assinatura de Webhooks:** Todos os webhooks de entrada (iFood, Stripe, MP) são validados via HMAC-SHA256 antes de qualquer processamento.
