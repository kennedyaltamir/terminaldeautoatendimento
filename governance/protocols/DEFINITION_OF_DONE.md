
# ✅ Definition of Done (DoD) Global — MesaFlow Enterprise

Este documento define os critérios obrigatórios para que qualquer tarefa seja considerada "Concluída" e elegível para merge na branch de produção.

---

## 1. Qualidade de Código
- [ ] **Type Safety:** 100% de cobertura TypeScript (sem `any`) e Python Type Hints.
- [ ] **Linting:** Zero erros no ESLint e Black/Flake8.
- [ ] **Async-First:** Todas as operações de I/O (DB, Redis, API) utilizam `async/await`.
- [ ] **Aritmética:** Valores monetários tratados exclusivamente como Inteiros (Centavos).

## 2. Segurança & Isolamento
- [ ] **Zero Trust:** Validação explícita de `company_id` em todos os pontos de entrada.
- [ ] **RLS Compliance:** Verificação de que a query não tenta bypassar o Row-Level Security.
- [ ] **Sanitização:** Inputs de texto processados contra XSS/Injection.

## 3. Testes & Validação
- [ ] **Unit Tests:** Cobertura mínima de 80% da lógica de negócio alterada.
- [ ] **Integration Tests:** Contratos de API validados via `TestClient`.
- [ ] **Proof of Work:** Script `verify_TASK-XXX.py` retornando `SUCCESS` em ambiente de Staging.

## 4. Documentação & Governança
- [ ] **Task Log:** Arquivo de log gerado em `docs/*/tasks/`.
- [ ] **ADR:** Se houver mudança arquitetural, ADR correspondente criada e aprovada.
- [ ] **Kernel Score:** `otimizar.py` reportando Score Global ≥ 95.
- [ ] **RFC Alignment:** Mudança em conformidade com as RFCs 001 a 010.

---
*Status: ENFORCED. Versão 1.0.*

