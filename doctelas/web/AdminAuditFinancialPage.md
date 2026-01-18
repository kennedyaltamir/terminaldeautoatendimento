# 💰 AdminAuditFinancialPage
> **Plataforma:** WEB | **Domínio:** FINTECH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela é o núcleo de integridade financeira do MesaFlow OS. Seu objetivo é permitir a conciliação bancária e a auditoria da cadeia de custódia (Ledger L7), garantindo que cada centavo transacionado no gateway (Mercado Pago/Stripe) tenha uma correspondência exata e imutável no banco de dados do sistema.

## 2. Estrutura e Layout (Arquitetura de Dados)
- **Integridade Banner:** Indicador visual do status da Hash Chain (Verde: Íntegro, Vermelho: Violado).
- **Reconciliation Table:** Comparativo entre o extrato do Gateway e o Ledger interno.
- **Orphan Transaction List:** Painel para identificação de transações que existem no provedor mas não foram processadas pelo sistema (ex: falha de webhook).

## 3. Elementos Interativos e Ações
- **Verify Chain:** Dispara o script `FIN-01` para validar matematicamente todos os hashes da tabela `financial_ledger`.
- **Fix Orphan:** Botão de ação manual para criar uma entrada corretiva no Ledger para transações órfãs validadas.
- **Export Ledger:** Gera um arquivo CSV assinado digitalmente para fins fiscais e contábeis.

## 4. Regras de Negócio e Estados
- **Imutabilidade:** Registros no Ledger não podem ser alterados ou deletados (Append-only).
- **Mismatch Alert:** O sistema destaca em laranja transações onde o valor recebido diverge do valor do pedido.
- **Loading State:** Spinner de alta precisão durante a verificação de integridade da cadeia.

## 5. Fluxos de Navegação
1. O auditor acessa o menu "Auditoria Financeira".
2. O sistema carrega o relatório de conciliação via `GET /api/admin/audit/financial/reconciliation`.
3. O usuário valida as divergências e aplica correções se necessário.

## 6. Documentação Técnica (API)
- **Endpoints:**
  - `GET /api/admin/audit/financial/ledger`
  - `POST /api/admin/audit/financial/fix-orphan`
  - `GET /api/admin/audit/financial/verify-integrity`

---
![Financial Audit Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-audit-fin.png)

