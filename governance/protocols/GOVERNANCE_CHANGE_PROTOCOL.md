<Content><![CDATA[
[[MESAFLOW_BEGIN:docs/governance/UPDATE_EXECUTION_PROTOCOL.md]]
# ⚙️ Update Execution Protocol (UEP)
# LAST_MODIFIED: 2026-01-08 00:50:00
# VERSION: 2.2

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
        *   `<Terminal_Commands>` (Obrigatório, pode ser vazio)
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
    [[MESAFLOW_END]]
    ]]]]><![CDATA[>
    </Content>
</File>
```

### 2.2 Regra de Omissão (FFP-02)
É terminantemente proibido o uso de `...`, `restante do código` ou qualquer forma de elipse. A entrega deve ser **byte-a-byte integral**.

---

## 3. Governança de Alteração (Granular Override)

Para alterar arquivos protegidos (Kernel ou `docs/governance/`), a IA deve declarar explicitamente quais caminhos ela tem autorização para modificar:

```xml
<Governance_Override>
    <File path="docs/governance/UPDATE_EXECUTION_PROTOCOL.md"/>
</Governance_Override>
```

Se o arquivo estiver na lista de proteção e não constar no `<Governance_Override>`, o executor abortará com **FFP-06**.

---

## 4. Assinatura de Sucesso
O executor `atualizar.py` emitirá `✨ Sincronia 100% concluída.` ao finalizar. Qualquer outra saída indica falha no processo.