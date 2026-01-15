# ⚙️ Update Execution Protocol (UEP)
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-14 21:15:00
# VERSION: 7.2 (Immune System Active)

## 1. Contrato de Resposta (XML Strict)
Toda resposta da IA deve conter a tag `<Knowledge_Accumulation>`.

## 2. Acúmulo de Conhecimento Persistente
O conteúdo dentro da tag `<Knowledge_Accumulation>` será anexado pelo `atualizar.py` ao arquivo `docs/technical/AI_KNOWLEDGE_BASE.md`.
- **Regra:** O conhecimento deve ser somado, nunca substituído.
- **Objetivo:** Criar uma memória imunológica que impeça a repetição de erros e o retrabalho.

## 3. Compatibilidade Windows (Encoding)
Todo script Python gerado deve conter o cabeçalho de resiliência Unicode para evitar `UnicodeEncodeError` em terminais Windows:
```python
import sys, io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 4. Estrutura Obrigatória
```xml
<Schema_Execution>
    <Execution_Result>
        <Files>...</Files>
        <Terminal_Commands>...</Terminal_Commands>
        <Knowledge_Accumulation>
            <![CDATA[
            ### [DATA] - [TITULO]
            - Aprendizado: ...
            - Prevenção: ...
            ]]]]><![CDATA[>
        </Knowledge_Accumulation>
    </Execution_Result>
</Schema_Execution>
