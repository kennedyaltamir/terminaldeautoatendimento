
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-13 03:20:00
# 📉 Relatório de Drift de Enums (Governança L6)

**Data:** 13/01/2026
**Executor:** Kernel L6
**Contexto:** Normalização do Protocolo INDA V10

## 1. Diagnóstico de Divergência
Foi detectada uma inconsistência estrutural crítica entre o estado atual do `registry.xml` e a Máquina de Estados Canônica definida no Protocolo INDA V10.

### Tabela de Mapeamento (De -> Para)

| Estado Atual (Legacy) | Estado Canônico (INDA V10) | Justificativa Técnica |
| :--- | :--- | :--- |
| `DONE` | **SUCCESS** | Padronização de término positivo. |
| `DONE_PASSIVE` | **SUCCESS** | O conceito de "passivo" deve ser um atributo do script, não do estado. |
| `FAIL` | **FAILED** | Padronização gramatical (Particípio). |
| `PASS` | **SUCCESS** | Unificação de terminologia de teste vs execução. |
| `BLOCKED` | **BLOCKED_BY_DATA** | Especificidade da causa do bloqueio (dependência de dados/infra). |
| `PENDING` | **PENDING** | *Compatível.* |
| `N/A` | **DEPRECATED** | Scripts obsoletos ou removidos. |

## 2. Arquivos Afetados
A normalização deve ser aplicada nos seguintes artefatos:

1.  **`comunication/registry.xml`** (Fonte da Verdade)
    - *Ação Requerida:* Migração em massa dos atributos `status="..."`.
2.  **`scripts/validar/master_readiness_check.py`**
    - *Ação Requerida:* Atualizar lógica de verificação de status (se houver hardcode).
3.  **`scripts/maintenance/governance_dashboard.py`**
    - *Ação Requerida:* Atualizar parsing de logs para contabilizar novos enums.

## 3. Risco de Migração
- **Baixo.** A alteração é puramente semântica e de metadados. Não afeta a lógica de execução dos scripts Python, apenas a orquestração.

## 4. Próximo Passo (Action Item)
Executar script de migração (a ser criado) para reescrever o `registry.xml` conforme a coluna "Estado Canônico".

---
*Relatório gerado para Auditoria L0.*

