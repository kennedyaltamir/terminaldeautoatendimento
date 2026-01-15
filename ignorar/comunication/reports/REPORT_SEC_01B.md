# 🔐 RLS Role Matrix Report (SEC-01B)

> **Observação:** Privilégios de catálogo sensível (`pg_authid`) não são acessíveis em ambientes gerenciados (Neon/RDS). A auditoria utiliza `pg_roles`, que é a fonte suportada oficialmente.

## Matriz de Poder
| Role | Superuser | Bypass RLS | Login |
| :--- | :---: | :---: | :---: |
| **cloud_admin** | 🔴 YES | 🚨 YES | ✅ |
| **mesaflow_app** | 🟢 NO | 🟢 NO | ✅ |


## Veredito Técnico
✅ **PASS:** Role `mesaflow_app` está corretamente restrita.
