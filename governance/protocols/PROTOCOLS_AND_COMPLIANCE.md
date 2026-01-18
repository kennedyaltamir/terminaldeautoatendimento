# 🏛️ Manual de Governança e Protocolos
**Domínio:** GOVERNANCE | **Versão:** 10.0 (INDA Standard)

## 1. Protocolo INDA (Ciclo de Vida)
Toda alteração no MesaFlow OS deve seguir:
1. **Inspection:** Auditoria do estado atual via `gerartxt.py`.
2. **Normalization:** Alinhamento com as RFCs 001-010.
3. **Decision:** Registro de decisão técnica (ADR).
4. **Action:** Aplicação via `atualizar.py` com geração de Prova de Trabalho (Script de Validação).

## 2. Protocolos de IA
- **AI_ROLE_PROTOCOL (ARP):** Define as fronteiras entre Architect (Estrategista) e Executor (Operário).
- **ROLLBACK_PROTOCOL:** Procedimento de emergência para reversão de mutações de código falhas.
- **TASK_LIFECYCLE_PROTOCOL:** Estados obrigatórios: OPEN -> SPECIFIED -> IN_PROGRESS -> VALIDATING -> DONE.

## 3. Matriz de Responsabilidades (RACI)
| Atividade | Architect | Executor | Reviewer | SRE |
| :--- | :---: | :---: | :---: | :---: |
| Mudança de Schema | Accountable | Responsible | Consulted | Informed |
| Hotfix de Produção | Consulted | Responsible | Accountable | Responsible |
| Auditoria RLS | Accountable | Informed | Responsible | Consulted |
| Deploy Final | Informed | Informed | Accountable | Responsible |

## 4. Scripts de Auditoria (Quality Gates)
- `SYS-01`: Validador de integridade estrutural de diretórios.
- `SEC-01`: Teste de estresse de isolamento RLS (Invasão lateral).
- `FIN-01`: Verificador de cadeia de custódia do Ledger.
- `MRC-01`: Master Readiness Check (O gate final de deploy).