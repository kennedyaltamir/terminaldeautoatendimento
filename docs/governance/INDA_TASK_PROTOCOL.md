# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-09 22:00:00
# 🧠 PROTOCOLO DE IMPLEMENTAÇÃO DE TASKS — KERNEL INDA

**Versão:** 1.7
**Classificação:** CONSTITUTIONAL_CORE
**Status:** ATIVO (LEI SUPREMA)

---

## 1. Definição de Kernel Fechado

O sistema opera em **Kernel Fechado**:
A Task é a única fonte de verdade.

### A Lei Suprema
> **Se não está escrito na Task, é PROIBIDO.**

A IA:
- Não pergunta
- Não interpreta
- Não supõe
- Não inventa boas práticas

---

## 2. Métrica de Suficiência (Validação de Task)

Uma task só é válida quando atende aos quatro critérios simultâneos:

1. **Execução Autônoma** — nenhum contato humano após início
2. **Validação Binária** — True/False somente
3. **Determinismo** — mesmo input → mesmo output
4. **Isolamento** — zero dependências fora da Task

---

## 3. Estrutura Obrigatória da Task (Template INDA)

### 1. IDENTIFICAÇÃO RÍGIDA
- `TASK_ID`
- `TITLE`
- `PRIORITY`
- `EXECUTION_MODE`

### 2. DETALHAMENTO PROFUNDO (OBRIGATÓRIO)
O arquivo `docs/TASKS.md` é a **Única Fonte de Verdade (SSOT)**.
Toda task listada nele DEVE possuir uma pasta correspondente em `docs/tasks/details/TASK-XXX/` contendo **no mínimo 3 arquivos explicativos**:
1. **Comportamento Esperado:** Descrição funcional detalhada.
2. **Plano de Verificação:** Como validar o sucesso (roteiro de teste e script).
3. **Documentação Técnica:** Specs de API, Schema de Banco ou Lógica de UI.

### 3. ESTADO ATUAL (BASELINE)
Descrição objetiva e verificável do estado anterior.

### 4. ESTADO FINAL DESEJADO (OBJETIVO)
Checklist binário de sucesso.

### 5. ESCOPO FECHADO
- **Inclui** o permitido.
- **Exclui** o proibido explicitamente.

### 6. RESTRIÇÕES TÉCNICAS
Linguagens, frameworks e permissões estruturais.

### 7. ENTRADAS GARANTIDAS
Somente as listadas podem ser utilizadas.

### 8. SAÍDAS ESPERADAS
Lista fechada de artefatos.

---

## 4. Protocolo de Conversação e Resposta

### 4.1 Modo de Ingestão (Non-Raw)
Toda resposta deve assumir que o usuário **NÃO** está em modo raw (Copy & Paste manual).
- **Obrigatoriedade:** Toda resposta deve conter um script que verifique o que foi proposto.
- **Fallback:** Se não houver lógica de negócio testável, gerar script para verificar a substituição do arquivo na pasta `scripts/verificationpaste/`.

### 4.2 Base de Conhecimento
- Toda resposta alimenta a base de conhecimento da próxima iteração.
- Toda task respondida deve gerar um **Documento de Redução da Task** (Resumo do que foi feito, por que e como manter).

### 4.3 Comandos Finais
Ao final de toda resposta, deve haver um bloco de comandos de terminal para:
1. Aplicar as mudanças (`python atualizar.py`).
2. Rodar validações.
3. **Commitar as alterações** (Git add/commit com mensagem padronizada).

### 4.4 Restrições de Resposta
- As respostas devem ser compatíveis com o parser do `atualizar.py`.
- Markdown específico e limpo.
- **Negar resumos:** A resposta deve ser completa.
- **Negar substituição de arquivos sensíveis:** `atualizar.py`, `docs/governance/*` e outros essenciais sem Override explícito.

---

## 5. Geração de Contexto (O Cérebro)

O script `gerartxt.py` é responsável por gerar a base de conhecimento concatenada.

### 5.1 Estrutura Lógica do Contexto
Os arquivos devem ser concatenados na seguinte ordem lógica para alimentar a IA:
1. **Comportamento/Persona:** Explicação sobre quem é a IA e suas regras.
2. **App:** Todos os arquivos do aplicativo Mobile.
3. **Site:** Todos os arquivos do Frontend.
4. **Documentação e Scripts:** O restante do sistema.

### 5.2 Ordem Prioritária do Bundle (Top 10)
Os primeiros arquivos do bundle DEVEM ser, nesta ordem estrita:
1. `docs/governance/AI_STARTUP_SEQUENCE.xml`
2. `docs/governance/CONTEXT_PRIORITY_PROTOCOL.md`
3. `docs/Prompts/System_Persona.xml`
4. `docs/governance/AI_ROLE_PROTOCOL.md`
5. `docs/governance/FAIL_FAST_PROTOCOL.md`
6. `docs/governance/UPDATE_EXECUTION_PROTOCOL.md`
7. `docs/governance/ERROR_RESPONSE_MAPPING_PROTOCOL.md`
8. `docs/TASKS.md`
9. `docs/ROADMAP.md`

### 5.3 Filtro de Ruído
É **PROIBIDO** concatenar arquivos inúteis (lockfiles, assets binários, caches) que possam contaminar a base de conhecimento.

---

## 6. Protocolo de Execução e Atualização (As Mãos)

O script `atualizar.py` é o agente de mudança e deve seguir critérios máximos de análise de risco.

### 6.1 Fluxo de Aplicação
1. Recebe o conteúdo colado em `resposta.txt` (sem raw mode).
2. Salva os arquivos propostos na pasta `Copy/` (respeitando a árvore de diretórios).
3. Abre Diff (VSCode) comparando `Copy/` com o arquivo real.
4. Aguarda confirmação (`s` para sim).
5. Aplica a substituição.

### 6.2 Proteção de Kernel
É **PROIBIDO** substituir automaticamente arquivos sensíveis sem `<Governance_Override>`:
- `atualizar.py`
- `docs/governance/*`
- `gerartxt.py`
- `.env`

---

## 7. Protocolo de Tratamento de Erros (Diagnóstico)

Sempre que uma execução de código resultar em erro, a IA deve seguir este fluxo obrigatório:

1. **Relatório de Incidente (MD):** Criar um arquivo Markdown detalhando:
   - Onde o erro ocorreu.
   - Arquivos envolvidos.
   - **5 Principais Hipóteses** de causa raiz.
2. **Script de Diagnóstico (Python):** Gerar um script que teste essas 5 hipóteses programaticamente.
3. **Resolução:** Baseado na saída do script de diagnóstico, gerar o script de correção ou os arquivos corrigidos.

---

## 8. Interconexão e Usabilidade

- **Interligação:** Todas as partes do projeto (Back, Front, Mobile, Docs) devem se referenciar corretamente. Links quebrados ou importações fantasmas são violações graves.
- **Usabilidade:** O sistema deve ser fácil e intuitivo de usar. Se uma configuração é complexa, deve haver um script facilitador ou documentação "How-to".

---

## 9. Vigência
Esta regra entra em vigor **IMEDIATAMENTE**. Qualquer desvio encontrado deve ser corrigido instantaneamente para adequação.
