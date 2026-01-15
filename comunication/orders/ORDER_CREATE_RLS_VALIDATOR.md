
# ORDEM DE SERVIÇO: CRIAÇÃO DE VALIDADOR RLS
**ID:** ORD-002
**Prioridade:** IMEDIATA (BLOQUEANTE)
**Alvo:** `scripts/validation/verify_TASK-SEC-01.py`

## Contexto
O pipeline de prontidão falha na etapa "RLS (Row-Level Security)" devido à ausência do script de validação. O RLS é um requisito crítico de segurança para sistemas multi-tenant.

## Especificação Técnica
O script deve:
1.  Conectar ao banco de dados (usando `app.database`).
2.  Criar dois tenants de teste (Empresa A e Empresa B).
3.  Inserir dados (ex: Pedidos) para a Empresa A.
4.  Tentar ler os dados da Empresa A usando o contexto da Empresa B.
5.  **Sucesso:** A query retorna 0 resultados (Bloqueio pelo Banco).
6.  **Falha:** A query retorna dados (Vazamento).
7.  Gerar relatório em `comunication/reports/RLS_VALIDATION_REPORT.md`.
8.  Ser compatível com Windows (UTF-8 stdout).

## Critério de Aceite
O comando `python scripts/validation/master_readiness_check.py` deve passar pela etapa de RLS e falhar na próxima (Security Headers), indicando progresso.

