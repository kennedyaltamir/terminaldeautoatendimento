# ⚠️ FAIL FAST PROTOCOL (FFP)
# LAST_MODIFIED: 2026-01-08 00:55:00
# VERSION: 1.1

## 1. Objetivo
Abortar imediatamente execuções malformadas para preservar a integridade do sistema MesaFlow e economizar recursos computacionais.

## 2. Gatilhos de Abortagem (FFP Codes)

| Código | Nome | Gatilho |
| :--- | :--- | :--- |
| **FFP-01** | **Ruído Estrutural** | Texto fora do XML ou tags fora da ordem canônica. |
| **FFP-02** | **Entrega Parcial** | Uso de placeholders ou omissões (`...`). |
| **FFP-03** | **Vácuo de Teste** | Task COMPLEXA sem arquivo de teste ou isenção clara. |
| **FFP-04** | **Ambiguidade** | Instruções que permitem múltiplas interpretações técnicas. |
| **FFP-05** | **Erro de Sintaxe** | Falha na compilação estática do código gerado. |
| **FFP-06** | **Ilegalidade** | Alteração em arquivos protegidos sem Override granular. |
| **FFP-07** | **Boot Incompleto** | IA respondeu antes de completar a `AI_STARTUP_SEQUENCE`. |

## 3. Resposta de Erro Padronizada
O executor deve responder estritamente no formato:

```xml
<ERROR code="FFP-XX" severity="CRITICAL|WARN">
    Descrição técnica e objetiva da falha.
</ERROR>
```

**Nota:** Nenhuma desculpa ou explicação adicional deve ser gerada após o bloco de erro.