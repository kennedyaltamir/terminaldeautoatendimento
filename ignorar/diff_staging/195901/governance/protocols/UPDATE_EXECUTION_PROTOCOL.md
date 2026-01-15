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
    