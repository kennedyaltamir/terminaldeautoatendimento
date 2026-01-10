# 📝 Code Change Protocol (CCP)

> **Versão:** 1.2
> **Classificação:** EXECUTION_STANDARD
> **Dependência:** `UPDATE_EXECUTION_PROTOCOL.md`

## 1. Objetivo
Padronizar como o código fonte do MesaFlow pode ser alterado, garantindo que toda linha de código tenha uma razão de existir rastreável e que a infraestrutura cognitiva seja preservada.

---

## 2. Regras de Alteração

### R1: Princípio da Missão Vinculada
Nenhuma linha de código pode ser alterada sem um `<Schema_Mission>` prévio aprovado pelo Architect.
- **Proibido:** "Vi um erro aqui e corrigi rapidinho".
- **Permitido:** "Conforme Missão 38, passo 2, ajustando a função X".

### R2: Imutabilidade Implícita
O Executor não tem permissão para "melhorar" código que não faz parte do escopo da missão.
- Refatorações estéticas, mudanças de linting ou otimizações não solicitadas são consideradas **Violações de Escopo**.

### R3: Entrega Atômica e Integral
- Arquivos modificados devem ser entregues **INTEIROS**.
- É estritamente proibido o uso de `// ...rest of code` ou placeholders.
- O código entregue deve ser capaz de substituir o arquivo original sem quebrar dependências.

### R4: Infraestrutura Cognitiva Protegida
Arquivos que afetam diretamente a geração de contexto para IAs são classificados como **Infraestrutura Cognitiva Crítica**.

Incluem, mas não se limitam a:
- `gerartxt.py`
- Regras de exclusão, inclusão ou priorização de arquivos.
- Protocolos que definem como o contexto é montado (`CONTEXT_GENERATION_PROTOCOL.md`).

➡️ Qualquer alteração nesses elementos é automaticamente classificada como **Nível 3 (Constitucional)** e segue rigorosamente o `GOVERNANCE_CHANGE_PROTOCOL`.

---

## 3. Fluxo de Aprovação de Código

1. **Especificação:** Architect define a mudança.
2. **Geração:** Executor gera o XML com o código.
3. **Validação Estática:** O script `atualizar.py` verifica a sintaxe básica e a presença de tags obrigatórias.
4. **Aplicação:** O código sobrescreve o arquivo local.
5. **Verificação:** Testes automatizados ou scripts de verificação rodam.

> **Nota:** Mudanças que impactam o contexto consumido por IAs devem ser avaliadas também sob o `CONTEXT_GENERATION_PROTOCOL.md`, além deste protocolo.

---

## 4. Tratamento de Dependências
Se uma mudança de código exige uma nova biblioteca:
1. A alteração deve incluir o `package.json` ou `requirements.txt`.
2. A alteração deve incluir o comando de instalação no `<Terminal_Commands>`.
3. A documentação (`TASKS.md`) deve ser atualizada.

---

## 5. Arquivos Protegidos (Immutable Core)

A alteração destes arquivos exige permissão elevada e justificativa explícita:

1. `atualizar.py` (Mecanismo de Aplicação).
2. `docs/governance/*.md` (Constituição).
3. `.gitignore` (Fronteira de Repositório).
4. `.env` (Segredos).
5. `gerartxt.py` (Infraestrutura Cognitiva).
6. `docs/governance/CONTEXT_GENERATION_PROTOCOL.md` (Regras de Contexto).
