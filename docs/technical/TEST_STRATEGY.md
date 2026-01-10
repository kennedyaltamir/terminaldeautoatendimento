# 🧪 Estratégia de Testes (QA Strategy)

## 1. Pirâmide de Testes
O MesaFlow adota uma estratégia equilibrada para garantir qualidade sem sacrificar velocidade.

### Nível 1: Testes Unitários (Backend)
- **Foco:** Lógica de negócios isolada (Cálculos financeiros, validação de estoque, regras de desconto).
- **Ferramenta:** `pytest`.
- **Cobertura Alvo:** 80% dos Services e Models.
- **Execução:** A cada commit (Local e CI).

### Nível 2: Testes de Integração (API)
- **Foco:** Contratos de API, fluxo de dados entre camadas (Router -> Service -> DB).
- **Ferramenta:** `pytest` + `TestClient` (FastAPI).
- **Banco de Dados:** SQLite em memória ou container Docker efêmero.
- **Execução:** No Pipeline de CI.

### Nível 3: Testes End-to-End (Frontend)
- **Foco:** Jornadas críticas do usuário (Fazer pedido, Fechar conta, KDS).
- **Ferramenta:** `Playwright`.
- **Cenários:**
    - Cliente faz pedido -> Cozinha recebe -> Garçom entrega.
    - Fluxo de pagamento Pix.
- **Execução:** Nightly builds ou antes de releases principais.

## 2. Dados de Teste
- Utilizamos `scripts/maintenance/seed.py` para popular o banco com dados determinísticos (Empresa "Hamburgueria do Zé") para testes manuais e E2E.

## 3. Critérios de Aceite (Green Build)
Nenhum código pode ser mergeado na `main` se:
1.  Houver falha em qualquer teste unitário.
2.  A cobertura de código cair significativamente.
3.  O linter (ESLint/Black) reportar erros.
