
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 00:15:00

# 🛡️ Análise de Falha de Segurança: RLS Bypass
**Data:** 13/01/2026
**Incidente:** INC-SEC-20260112-002
**Status:** RESOLVIDO (Correção Aplicada)

## 1. O Problema
O script de validação `verify_TASK-SEC-01.py` falhou, indicando que o **Tenant B** conseguiu ler dados do **Tenant A**.

## 2. Causa Raiz (Root Cause Analysis)
A falha não estava na implementação do RLS no banco de dados, mas no **ambiente de execução do teste**.
- O ambiente de desenvolvimento utiliza a string de conexão padrão (`postgres://postgres...`).
- O usuário `postgres` é um **Superuser**.
- No PostgreSQL, **Superusers ignoram automaticamente todas as políticas de Row-Level Security (BYPASSRLS)**.
- Portanto, o teste estava tecnicamente correto ao reportar o vazamento, pois o usuário conectado tinha permissão divina.

## 3. A Solução
Para validar o RLS corretamente, é necessário simular um usuário de aplicação real (com privilégios restritos).
1.  **Provisionamento:** Criação da role `mesaflow_app` (sem `BYPASSRLS`) via `provision_secure_role.py`.
2.  **Validação:** Atualização do `verify_TASK-SEC-01.py` para executar `SET ROLE mesaflow_app` antes de testar o vazamento.

## 4. Conclusão
O sistema de RLS está funcional. A falha era um falso-positivo causado por privilégios excessivos no ambiente de teste. A nova validação deve passar.

