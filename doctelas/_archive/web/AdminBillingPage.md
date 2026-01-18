# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:35:00
# 🖥️ AdminBillingPage
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/admin/[slug]/settings/billing`
> **Acesso:** Protected (Owner)
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Gestão da assinatura do software (SaaS). Upgrade de plano, histórico de faturas e método de pagamento.
**Persona Principal:** Dono.

## 2. Estrutura de Interface
- **Layout Pai:** `AdminLayout`.
- **Componentes Chave:**
  - `PlanCard`: Detalhes do plano atual (Free/Pro/Enterprise).
  - `UsageMetrics`: Barra de progresso de uso (ex: Pedidos/mês).
  - `BillingHistory`: Tabela de faturas passadas.

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `Fazer Upgrade` | Button | `handleUpgrade` | Redireciona Stripe | Checkout Session |
| `Gerenciar Assinatura` | Button | `handlePortal` | Redireciona Stripe | Billing Portal |

## 4. Estados da Tela
- **Free:** Mostra limites e CTA para Upgrade.
- **Pro:** Mostra status "Ativo" e botão de gestão.
- **Past Due:** Alerta vermelho de pagamento pendente.

## 5. Fluxos de Navegação
1. **Entrada:** Configurações -> Faturamento.
2. **Saída:** Portal do Stripe (Externo).

## 6. Regras de Negócio Críticas
- [x] Integração segura com Stripe Customer Portal.
- [x] Bloqueio de recursos se o plano Free exceder limites.

## 7. Dados & Integração
- **API Endpoints:**
  - `POST /api/admin/billing/upgrade`
  - `POST /api/admin/billing/portal`

