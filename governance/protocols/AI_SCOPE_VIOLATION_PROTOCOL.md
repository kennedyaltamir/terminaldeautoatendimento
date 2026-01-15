# 🚫 AI Scope Violation Protocol (ASVP)

> **Versão:** 1.0
> **Classificação:** SECURITY_BOUNDARY

## 1. Objetivo
Definir os critérios para identificar, classificar e remediar violações de escopo por parte das IAs operantes.

---

## 2. Tipos de Violação

### Nível 1: Drift Cognitivo (LOW)
Quando a IA começa a misturar tons ou responsabilidades leves.
- **Exemplo:** O Executor adiciona um comentário explicativo excessivo no código ("Aqui eu fiz isso porque...").
- **Ação:** Warning no próximo prompt. Aceite condicional.

### Nível 2: Contaminação de Papel (HIGH)
Quando a IA executa ações de outro papel.
- **Exemplo:**
    - O Architect escreve o código final do arquivo.
    - O Didactic tenta corrigir um bug no código durante a explicação.
- **Ação:** **REJEIÇÃO IMEDIATA**. O output é descartado. Solicita-se regeneração com reforço de persona.

### Nível 3: Quebra de Governança (CRITICAL)
Quando a IA viola regras de segurança ou integridade.
- **Exemplo:**
    - O Executor altera o `atualizar.py`.
    - Qualquer IA inventa arquivos que não existem no contexto.
    - O Executor tenta explicar algo para o usuário em texto plano fora do XML.
- **Ação:** **ROLLBACK IMEDIATO**. O estado do projeto é revertido. A sessão da IA deve ser encerrada/resetada.

---

## 3. Procedimento de Detecção e Correção

1. **Ingestão:** O sistema (ou o humano) lê a resposta.
2. **Scan:** Verifica-se a presença de tags obrigatórias (`<Task_Classification>`, `<Domain>`).
3. **Análise de Conteúdo:**
    - Se Executor: Há texto fora das tags XML? -> **Violação**.
    - Se Architect: Há código executável fora de blocos de exemplo? -> **Violação**.
4. **Veredito:**
    - Se **PASS**: Aplica-se a mudança.
    - Se **FAIL**: Dispara-se o gatilho de correção (Prompt de Correção).

## 4. Prompt de Correção Padrão
> "REPROVADO. Violação de Escopo Nível [X]. Você é [PAPEL], mas agiu como [OUTRO PAPEL]. Retorne ao seu kernel e execute apenas [AÇÃO PERMITIDA]."
