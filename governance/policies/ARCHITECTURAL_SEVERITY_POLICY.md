# ⚖️ Architectural Severity Policy
**Version:** 1.0.0
**Domain:** SECURITY / ARCHITECTURE

Define as permissões de alteração de código baseadas no diagnóstico do Cognitive Scanner.

| Severidade | Impacto | Regra de Mutação |
| :--- | :--- | :--- |
| **CRITICAL** | Bloqueante | **Proibido** alterar sem ADR formal e aprovação de Arquiteto Humano. |
| **HIGH** | Risco | Alteração permitida apenas se o objetivo for a **resolução direta** da falha. |
| **MEDIUM** | Atenção | Alteração permitida via fluxo padrão de Task. |
| **LOW** | Cosmético | Alteração livre, desde que não aumente a complexidade. |

## 🚫 Trava de Segurança
Qualquer tentativa de ignorar uma falha `CRITICAL` para implementar uma nova feature resultará em **Veto de Kernel**.

