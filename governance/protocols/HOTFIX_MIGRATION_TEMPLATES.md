# 📋 Templates Adicionais de Governança
**Versão:** 5.0.2-SEQ | **Domínio:** GOVERNANCE

## 1. Template: Hotfix de Produção (CRITICAL)
```markdown
# HOTFIX-[ID]: [Descrição]
**Incidente Relacionado:** [Link Sentry/Issue]
**Causa Raiz:** [Análise Técnica]
**Impacto:** [Tenants Afetados / Risco Financeiro]
**Correção:** [Arquivos Alterados]
**Validação:** [Script de Teste E2E]
**Aprovação:** Optimus Kernel L6
```

## 2. Template: Database Migration (Alembic)
```markdown
# MIG-[ID]: [Título da Mudança]
**Tabelas Afetadas:** [Lista]
**Impacto RLS:** [Sim/Não - Se sim, descrever nova política]
**Downgrade Path:** [Comando SQL de reversão]
**Integridade:** [Hash do script .py]