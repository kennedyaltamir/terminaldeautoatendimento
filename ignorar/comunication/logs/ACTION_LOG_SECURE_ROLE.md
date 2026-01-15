
# LOG DE AÇÃO: PROVISIONAMENTO DE ROLE SEGURA
**Data:** 13/01/2026
**Executor:** Kernel-INDA
**Task:** SECURE-ROLE-SETUP

## 1. Ação Realizada
Criação de infraestrutura para teste de RLS com usuário não-superuser.

## 2. Detalhes Técnicos
- **Script SQL:** `scripts/migrations/setup_secure_role.sql` cria `mesaflow_app`.
- **Provisionador:** `scripts/maintenance/provision_secure_role.py` aplica o SQL.
- **Validador:** `verify_TASK-SEC-01.py` atualizado para usar `SET ROLE mesaflow_app`.

## 3. Justificativa
O usuário padrão `postgres` possui `BYPASSRLS`, o que invalida testes de segurança. A criação de um usuário restrito é mandatória para validação real.

## 4. Próximos Passos
Executar:
1. `python scripts/maintenance/provision_secure_role.py`
2. `python scripts/validation/verify_TASK-SEC-01.py`

