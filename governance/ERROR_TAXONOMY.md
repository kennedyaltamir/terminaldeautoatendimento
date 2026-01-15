# 🚨 MesaFlow Error Taxonomy
**Status:** ACTIVE
**Version:** 1.0

Esta taxonomia padroniza os códigos de erro emitidos pelo Kernel e seus subsistemas.

## 1. Fail-Fast Protocol (FFP) - Erros de Input/Output
| Código | Significado | Ação do Kernel |
| :--- | :--- | :--- |
| `FFP-01` | Ruído Estrutural (Texto fora do XML) | Rejeição Total |
| `FFP-02` | Omissão de Código (Placeholders) | Rejeição do Arquivo |
| `FFP-05` | Erro de Sintaxe (AST Parse Fail) | Rejeição do Arquivo |
| `FFP-06` | Violação de Segurança (Arquivo Protegido) | Bloqueio Crítico |

## 2. Kernel Internal Errors (KIE) - Erros de Sistema
| Código | Significado | Ação do Kernel |
| :--- | :--- | :--- |
| `KIE-01` | Falha de Snapshot (IO Error) | Abortar Operação |
| `KIE-02` | Falha de Integridade (Hash Mismatch) | Rollback Imediato |
| `KIE-03` | Corrupção de Journal | Reset do Log (Backup) |

## 3. Cognitive Warnings (CW) - Alertas do Optimizer
| Código | Significado | Ação Sugerida |
| :--- | :--- | :--- |
| `CW-01` | Alta Complexidade Ciclomática | Refatorar Módulo |
| `CW-02` | Arquivo Gigante (>400 linhas) | Dividir Arquivo |
| `CW-03` | Drift Arquitetural | Atualizar Docs |
