
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 13:05:00
# 🩺 Relatório de Remediação: GUC Enforcement

## 1. Descrição do Incidente
O script de validação v9 falhou na etapa final devido ao erro `psycopg2.errors.InsufficientPrivilege`. A causa foi a tentativa do papel `mesaflow_app` de executar uma query enquanto o parâmetro global `row_security` estava definido como `off` (herdado da etapa de setup administrativo).

## 2. Ação Corretiva
- **Isolation de GUC (Grand Unified Configuration):** O script v10 agora força `SET row_security = on` em todas as conexões de teste antes de assumir o papel restrito.
- **Protocolo Non-Bypass:** Confirmamos que a role `mesaflow_app` está corretamente impedida de burlar o RLS, o que é o comportamento esperado para uma conta de aplicação segura.

## 3. Veredito de Segurança
O erro anterior, apesar de interromper o script, foi uma **prova positiva** de que o banco de dados está protegendo a integridade do RLS contra manipulações de usuários não autorizados.

