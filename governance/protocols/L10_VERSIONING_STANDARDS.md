# 🏛️ Padrões de Versão e Rastreabilidade L10
**Versão:** 10.0.1-AUTO | **Domínio:** GOVERNANCE | **Status:** ENFORCED

## 1. Nomenclatura de Versão
- **Padrão:** `v<MAJOR>.<MINOR>.<PATCH>-<STATUS>`
- **Status:**
    - `AUTO`: Alteração realizada por IA com validação autônoma.
    - `SEALED`: Versão homologada para produção.
    - `EMERGENCY`: Hotfix aplicado fora do ciclo normal.

## 2. Rastreabilidade Automática
Toda Task no `TASKS.md` deve conter o link para a ADR correspondente:
- `[ ] TASK-FIN-05: Implementar ERP v2.0 (Ref: ADR-005)`
O script `atualizar.py` agora valida a existência da ADR antes de permitir o commit da task.

## 3. Templates de Hotfix e Rollback
- **Hotfix:** Exige `Post-Mortem` automático gerado pelo Sentry.
- **Rollback:** Deve incluir o `ImpactReport` detalhando quais dados foram afetados durante a janela de erro.