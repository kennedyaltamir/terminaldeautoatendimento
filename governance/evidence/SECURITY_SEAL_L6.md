
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 13:25:00
# 🛡️ SELO DE SEGURANÇA MESAFLOW L6

O sistema de isolamento **Row-Level Security (RLS)** foi exaustivamente testado e validado sob o protocolo **INDA Strict**.

## 🛡️ Camadas de Defesa Ativas
1.  **Session Binding:** Injeção de `app.current_company_id` em cada transação SQL.
2.  **Associative Isolation:** Tabelas dependentes (produtos, itens) isoladas via subqueries em nível de banco.
3.  **Owner Enforcement:** RLS forçado mesmo para usuários proprietários das tabelas (`FORCE RLS`).
4.  **Least Privilege:** Role `mesaflow_app` provisionada sem permissão de `BYPASSRLS`.

## 🚦 Status de Prontidão
O domínio **SECURITY** é declarado **GOLD MASTER READY**.
O isolamento é imutável e inegociável em nível de motor PostgreSQL.

---
*MesaFlow Kernel L6 — Security Sealed.*

