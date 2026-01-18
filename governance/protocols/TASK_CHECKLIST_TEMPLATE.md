# 📋 Template de Checklist de Execução — TASK-XXX

> **Título da Task:** [Breve descrição]
> **Status:** [OPEN | IN_PROGRESS | VALIDATING | DONE]

## 1. Pré-requisitos (INDA Phase: Inspection)
- [ ] Contexto carregado via `gerartxt.py`.
- [ ] Dependências identificadas e instaladas.
- [ ] Variáveis de ambiente configuradas no `.env`.

## 2. Implementação (INDA Phase: Action)
- [ ] Código escrito seguindo o **DoD Global**.
- [ ] Uso de `Decimal` ou Inteiros para valores financeiros.
- [ ] Validação de `company_id` em todas as novas queries.
- [ ] Nenhuma omissão de código (`...`) nos arquivos entregues.

## 3. Validação (INDA Phase: Verification)
- [ ] Script `scripts/validation/verify_TASK-XXX.py` criado.
- [ ] Execução do script retorna `exit code 0`.
- [ ] Testes unitários cobrem > 80% da nova lógica.

## 4. Encerramento (Governance Consolidation)
- [ ] Log de task gerado em `docs/*/tasks/`.
- [ ] `otimizar.py` reporta Score Global ≥ 95.
- [ ] Documentação técnica (PRD/SDS) atualizada.

---
*Gerado automaticamente pelo Kernel. Versão 1.0.*