# 📚 Documentation Standard Protocol (DSP)

> **Versão:** 1.0
> **Classificação:** KNOWLEDGE_MANAGEMENT

## 1. Objetivo
Padronizar a criação e manutenção de documentação para garantir que o conhecimento sobreviva à troca de contexto das IAs.

---

## 2. Estrutura Obrigatória de Arquivos .md

Todo arquivo Markdown deve iniciar com um cabeçalho de metadados (Frontmatter-like ou Tabela):

```markdown
# 📝 Título do Documento
> **Domínio:** [MOBILE | BACKEND | FRONTEND]
> **Tipo:** [TASK | DECISION | GUIDE]
> **Status:** [DRAFT | APPROVED | DEPRECATED]
```

## 3. Regras de Escrita

### 3.1 Clareza e Objetividade
- Use voz ativa ("O sistema processa..." em vez de "É processado pelo sistema...").
- Evite "futuro do pretérito" ("Deveria fazer"). Se não faz, é bug ou backlog.

### 3.2 Versionamento Humano
- Documentos vivos (`ROADMAP.md`, `TASKS.md`) devem ter um log de alterações no final ou usar marcações de data nas seções.

### 3.3 Referências Cruzadas
- Sempre linkar arquivos relacionados. Ex: "Conforme definido em `docs/governance/AI_ROLE_PROTOCOL.md`".

## 4. Taxonomia de Pastas
- `docs/governance/`: Leis e Regras.
- `docs/architecture/`: Decisões técnicas e diagramas.
- `docs/tasks/`: Logs de execução (Legado/Web).
- `docs/mobile/tasks/`: Logs de execução Mobile.
- `docs/reports/`: Relatórios de auditoria e incidentes.
