# ⚙️ Update Execution Protocol (UEP)
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-14 19:55:00
# VERSION: 2.3
> **Status:** CONSTITUCIONAL
> **Executor:** `atualizar.py` v2.1+
---

## 1. Estrutura Canônica de Resposta (XML-Strict)

A resposta da IA deve ser um envelope XML puro. **Qualquer texto fora das tags resulta em FFP-01 (ABORT).**

### 1.1 Ordem Obrigatória das Tags:

1.  `<Task_Classification>` (TRIVIAL ou COMPLEXA)
2.  `<Domain>` (Contexto da alteração)
3.  `<Schema_Execution>`
    *   `<Execution_Result>`
        *   `<Files>` (Lista de objetos `<File>`)
        *   `<Terminal_Commands>` (OBRIGATÓRIO: Lista de comandos para aplicar/validar)
        *   `<Expected_Terminal_Output>` (Assinatura de sucesso)
        *   `<Governance_Override>` (Opcional, granular)

---

## 2. Regras de Escrita de Arquivos

### 2.1 O Bloco de Conteúdo
Cada arquivo deve ser encapsulado em CDATA e usar as tags de transporte:

```xml
<File>
    <Path>caminho/do/arquivo.ext</Path>
    <Content><![CDATA[
    [[MESAFLOW_BEGIN:caminho/do/arquivo.ext]]
    ... conteúdo integral ...
    