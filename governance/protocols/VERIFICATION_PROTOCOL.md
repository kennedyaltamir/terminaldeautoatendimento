# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-09 22:00:00
# 🧪 Verification Protocol (VP)

**Versão:** 1.4
**Classificação:** QUALITY_ASSURANCE
**Dependência:** `INDA_TASK_PROTOCOL.md`

## 1. Objetivo
Eliminar a subjetividade na entrega de tarefas. Uma missão só é considerada cumprida se passar por critérios objetivos de verificação automatizada.

---

## 2. Taxonomia de Scripts de Verificação

Os scripts de verificação devem ser organizados rigorosamente conforme sua função nas pastas abaixo:

### A. `scripts/verificationpaste/` (Verificação de Arquivo)
- **Objetivo:** Confirmar se o arquivo foi criado ou substituído corretamente após o uso do `atualizar.py`.
- **Uso:** Obrigatório para toda resposta que gere código, caso não haja lógica de negócio testável.
- **Exemplo:** Verificar hash, existência do arquivo ou string específica.

### B. `scripts/validation/` (Verificação de Task - Proof of Work)
- **Objetivo:** Verificar se a Task cumpriu seu objetivo de negócio/técnico.
- **Exemplo:** Se a task era "Inserir usuário no banco", este script conecta no banco e faz um SELECT para confirmar a inserção.
- **Regra:** Deve retornar Exit Code 0 em caso de sucesso.

### C. `scripts/alignment/` (Verificação de Alinhamento)
- **Objetivo:** Pasta central de saúde do projeto.
- **Escopo:** Checagem de segurança, integridade de layout, consistência de banco de dados, sincronização entre módulos.
- **Periodicidade:** Deve ser atualizada e rodada periodicamente. Se um script aqui falhar, o projeto está desalinhado.
- **Regra:** Todos os scripts desta pasta DEVEM funcionar necessariamente.

### D. `scripts/verify/` (Conferência Simples)
- **Objetivo:** Scripts utilitários de conferência rápida que não agregam valor à base de conhecimento de longo prazo.
- **Tratamento:** Podem ser ignorados pelo `gerartxt.py` para não poluir o contexto.

---

## 3. Critérios de Sucesso (Definition of Done)

Para uma missão ser marcada como `[x]` no `TASKS.md`, ela deve atender a **todos** os critérios abaixo:

1. **Integridade de Arquivos:** Todos os arquivos listados na missão foram criados/modificados.
2. **Sintaxe:** O código não contém erros de sintaxe (validado por linter/compilador).
3. **Prova de Trabalho (Proof of Work):** Existe um script de verificação dedicado (`scripts/validation/verify_TASK-XXX.py`) que retorna `exit code 0`.
4. **Documentação de Redução:** Um documento resumindo a task foi gerado para a base de conhecimento.
5. **Detalhamento Prévio:** A task possuía os 3 arquivos obrigatórios em `docs/tasks/details/`.

## 4. Fluxo de Diagnóstico de Erro

Conforme definido no INDA Protocol v1.7:
1. **Erro Detectado.**
2. **Relatório MD Gerado** (Causa, Arquivos, 5 Hipóteses).
3. **Script de Diagnóstico** (Testa as hipóteses).
4. **Correção Aplicada.**

## 5. Procedimento de Falha
Se a verificação falhar:
1. **NÃO** marque a task como concluída.
2. Registre o erro no log da missão.
3. Acione o Executor para correção (Fix) seguindo o fluxo de diagnóstico.
4. Se a correção falhar 3 vezes -> **Rollback**.
