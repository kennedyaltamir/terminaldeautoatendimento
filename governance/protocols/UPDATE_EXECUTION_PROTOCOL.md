# ⚙️ Update Execution Protocol (UEP)
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-14 20:00:00
# VERSION: 7.0 (Unified Kernel)
> **Status:** CONSTITUCIONAL
> **Executor:** `atualizar.py` (MesaFlow Kernel v7+)
> **Entrada Oficial:** `resposta.txt`

---

## 1. Objetivo e Filosofia
Este protocolo define o funcionamento do **MesaFlow Kernel Executor**, um sistema operacional cognitivo que orquestra o **Ciclo INDA** (Input, Neural, Decision, Action).

O objetivo é garantir integridade, segurança e durabilidade (ACID) em cada intervenção no código, exigindo que a IA forneça não apenas o código, mas também os comandos para aplicá-lo e validá-lo.

---

## 2. O Ciclo INDA (Kernel Pipeline)
O executor opera em fases estritas. A falha em qualquer fase aborta a operação e aciona o Rollback automático.

### Fase 1: BOOT & RECEIVE
- O Kernel inicializa uma sessão única (`session_id`).
- Carrega o arquivo `resposta.txt`.
- Valida a estrutura XML (`<Schema_Execution>`).

### Fase 2: ANALYZE (HyperOptimus Agent)
Antes de tocar no disco, o agente realiza **Análise Estática (AST)**:
1.  **Validação Sintática:** Verifica se o código Python/JS é válido.
2.  **Carga Cognitiva:** Calcula a complexidade da árvore sintática.
3.  **Integridade:** Verifica a presença de placeholders proibidos (ex: elipses, comentários de "resto do código").

### Fase 3: PLAN & SECURITY
- Verifica permissões de escrita contra a lista `PROTECTED_EXACT_FILES`.
- Se um arquivo protegido (ex: `atualizar.py`, `governance/*`) for alvo sem `<Governance_Override>`, o plano é rejeitado.

### Fase 4: APPLY (Transaction Manager)
- **Snapshot Cognitivo (KSP):** Backup inteligente é criado em `backups/`.
- **Staging:** Arquivos originais são movidos para área temporária.
- **Write:** O novo conteúdo é escrito atomicamente.

### Fase 5: REPORT
- Emite um relatório final com Score de Integridade e status da transação.

---

## 3. Contrato de Resposta (XML Strict)

A resposta da IA deve ser um envelope XML puro. **Qualquer texto fora das tags resulta em FFP-01 (ABORT).**

### 3.1 Ordem Obrigatória das Tags:

1.  `<Task_Classification>` (TRIVIAL ou COMPLEXA)
2.  `<Domain>` (Contexto da alteração)
3.  `<Schema_Execution>`
    *   `<Execution_Result>`
        *   `<Files>` (Lista de objetos `<File>`)
        *   `<Terminal_Commands>` (OBRIGATÓRIO: Lista de comandos para aplicar/validar)
        *   `<Expected_Terminal_Output>` (Assinatura de sucesso)
        *   `<Governance_Override>` (Opcional, granular)

---

## 4. Regras de Escrita de Arquivos

### 4.1 O Bloco de Conteúdo
Cada arquivo deve ser encapsulado em CDATA e usar as tags de transporte:

```xml
<File>
    <Path>caminho/do/arquivo.ext</Path>
    <Content><![CDATA[
    [[MESAFLOW_BEGIN:caminho/do/arquivo.ext]]
    (CONTEÚDO INTEGRAL DO ARQUIVO AQUI)
    
# ⚙️ Update Execution Protocol (UEP)
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-14 21:00:00
# VERSION: 7.1 (Knowledge-Aware)

## 1. Contrato de Resposta (XML Strict)
Toda resposta da IA deve conter a tag `<Knowledge_Accumulation>`.

## 2. Acúmulo de Conhecimento Persistente
O conteúdo dentro da tag `<Knowledge_Accumulation>` será anexado pelo `atualizar.py` ao arquivo `docs/technical/AI_KNOWLEDGE_BASE.md`.
- **Regra:** O conhecimento deve ser somado, nunca substituído.
- **Objetivo:** Criar uma memória imunológica que impeça a repetição de erros e o retrabalho.

## 3. Estrutura Obrigatória
```xml
<Schema_Execution>
    <Execution_Result>
        <Files>...</Files>
        <Terminal_Commands>...</Terminal_Commands>
        <Knowledge_Accumulation>
            <![CDATA[
            ### [DATA] - [TITULO]
            - O que foi aprendido: ...
            - O que não quebrar: ...
            - Padrão de correção: ...
            ]]]]><![CDATA[>
        </Knowledge_Accumulation>
    </Execution_Result>
</Schema_Execution>
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
# ⚙️ Update Execution Protocol (UEP)
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-14 21:20:00
# VERSION: 8.0 (Unified Kernel & Immune System)

> **Status:** CONSTITUCIONAL
> **Executor:** `atualizar.py` (MesaFlow Kernel v8+)
> **Entrada Oficial:** `resposta.txt`

---

## 1. Objetivo e Filosofia
Este protocolo define o funcionamento do **MesaFlow Kernel Executor**, um sistema operacional cognitivo que orquestra o **Ciclo INDA** (Input, Neural, Decision, Action). O objetivo é garantir integridade, segurança e durabilidade (ACID) em cada intervenção no código.

## 2. O Ciclo INDA (Kernel Pipeline)
O executor opera em fases estritas. A falha em qualquer fase aborta a operação e aciona o Rollback automático.
1. **BOOT & RECEIVE:** Inicializa sessão e valida estrutura XML.
2. **ANALYZE:** Realiza Análise Estática (AST) e verifica placeholders proibidos (`...`).
3. **PLAN & SECURITY:** Verifica permissões contra `PROTECTED_EXACT_FILES`.
4. **APPLY:** Cria Snapshot (KSP) e realiza escrita atômica.
5. **VERIFY:** Valida SHA-256 do disco vs memória.
6. **REPORT:** Emite Score de Integridade e status da transação.

## 3. Contrato de Resposta (XML Strict)
A resposta da IA deve ser um envelope XML puro. **Qualquer texto fora das tags resulta em ABORT.**

### 3.1 Tags Obrigatórias e Ordem:
1. `<Task_Classification>`: TRIVIAL ou COMPLEXA.
2. `<Domain>`: Contexto da alteração.
3. `<Schema_Execution>`: Container mestre.
4. `<Execution_Result>`: Resultado da execução.
5. `<Files>`: Lista de objetos `<File>`.
6. `<Terminal_Commands>`: Lista de comandos para aplicar/validar.
7. `<Knowledge_Accumulation>`: Bloco de aprendizado persistente.

## 4. Regras de Escrita e Resiliência
### 4.1 Omissão Proibida (FFP-02)
É terminantemente proibido o uso de elipses (`...`) ou comentários de "resto do código". A entrega deve ser integral.

### 4.2 Compatibilidade Windows (Encoding)
Todo script Python gerado deve conter o cabeçalho de resiliência Unicode:
```python
import sys, io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### 4.3 Acúmulo de Conhecimento
O conteúdo de `<Knowledge_Accumulation>` será anexado ao arquivo `docs/technical/AI_KNOWLEDGE_BASE.md`. O conhecimento deve ser somado, nunca substituído, criando uma memória imunológica contra retrabalho.

---
**Assinatura:** MesaFlow Kernel L6.
