# 💰 Módulo: Financeiro & Marketing
**Rotas:** `/admin/[slug]/audit/financial` | `/admin/[slug]/marketing`

## 1. Auditoria Financeira
- **Intenção:** Prover transparência absoluta sobre o fluxo de caixa e integridade do banco.
- **Elementos:**
    - **Integrity Badge:** Indicador visual do status da Hash Chain.
    - **Ledger Table:** Lista de transações (ID, Valor, Hash, Referência).
    - **Reconciliation Panel:** Comparativo entre sistema e gateway.
- **Comportamento:** Bloqueia qualquer tentativa de edição. Se um hash divergir, o sistema entra em modo de alerta.

## 2. Marketing & Promoções
- **Intenção:** Gestão de cupons e campanhas de fidelidade.
- **Elementos:**
    - **Coupon Form:** Nome, Código, Tipo (Fixo/%), Valor, Validade.
    - **Usage Stats:** Contador de quantas vezes o cupom foi usado.
- **Comportamento:** Valida unicidade do código por Tenant.
- **API:** `GET /api/admin/marketing/promotions`.

