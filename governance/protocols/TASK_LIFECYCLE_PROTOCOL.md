# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 05:35:00
# 🔄 Task Lifecycle Protocol (TLP)

> **Versão:** 1.1
> **Classificação:** PROCESS_MANAGEMENT

## 1. Objetivo
Definir os estados possíveis de uma tarefa e os critérios para transição, evitando tarefas "zumbis" ou falsos positivos.

---

## 2. Estados da Tarefa

1. **OPEN (Aberta):** Definida no Roadmap, mas sem Missão criada.
2. **SPECIFIED (Especificada):** Missão criada pelo Architect (`<Schema_Mission>`).
3. **IN_PROGRESS (Em Execução):** Executor gerou o código (`<Schema_Execution>`).
4. **VALIDATING (Validando):** Código aplicado, aguardando execução do script de validação.
5. **DONE (Concluída):** Script de validação retornou `SUCCESS`, documentação atualizada.
6. **BLOCKED (Bloqueada):** Impedimento técnico ou de negócio identificado.

## 3. Fluxo de Transição

### De OPEN para SPECIFIED
- **Responsável:** Architect.
- **Requisito:** Definição clara de objetivo e arquivos afetados.

### De SPECIFIED para IN_PROGRESS
- **Responsável:** Executor.
- **Requisito:** Recebimento do `<Schema_Mission>`.

### De IN_PROGRESS para VALIDATING
- **Responsável:** Executor/Sistema.
- **Requisito:** Aplicação do código via `atualizar.py`.
- **Ação:** Criação obrigatória do arquivo `scripts/validation/verify_TASK-XXX.py`.

### De VALIDATING para DONE
- **Responsável:** Reviewer/Script.
- **Requisito:** Execução bem-sucedida de `python scripts/validation/verify_TASK-XXX.py`.
- **Ação:** Marcar `[x]` no `TASKS.md` e gerar log na pasta `docs/*/tasks/`.

## 4. Encerramento
Uma task só morre quando gera um **Artefato de Conclusão** (Código commitado + Doc atualizada + Script de Validação Passando). Tasks abandonadas devem ser movidas para o Backlog ou marcadas como CANCELLED.
