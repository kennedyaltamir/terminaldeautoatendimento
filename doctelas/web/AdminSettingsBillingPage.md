# 💳 AdminSettingsBillingPage
> **Plataforma:** WEB | **Domínio:** SAAS | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Central de faturamento e gestão de planos. Permite ao lojista realizar o upgrade para o plano Pro, gerenciar métodos de pagamento, visualizar faturas passadas e controlar o consumo de recursos do SaaS.

## 2. Estrutura e Componentes
- **Plan Comparison:** Cards detalhando os benefícios do plano atual vs planos superiores.
- **Usage Monitor:** Gráficos de consumo (ex: "45 de 50 pedidos gratuitos utilizados").
- **Billing History:** Lista de faturas pagas com link para download de recibos.

## 3. Elementos Interativos
- **Upgrade Trigger:** Inicia o fluxo de checkout seguro via Stripe.
- **Customer Portal Link:** Redireciona para o portal de autoatendimento do Stripe para troca de cartão de crédito.
- **Cancel Subscription:** Fluxo de cancelamento com pesquisa de satisfação integrada.

## 4. Regras de Negócio (SaaS)
- **Prorata Logic:** O sistema calcula automaticamente a diferença de valores em upgrades no meio do ciclo.
- **Grace Period:** Mantém o acesso Pro por 3 dias após falha no pagamento antes do bloqueio total.
- **Metered Billing:** Registro de uso para cobrança de taxas variáveis (se aplicável ao plano).

## 5. Estados de UI
- **Active:** Status normal de assinatura.
- **Past Due:** Alerta de pagamento pendente com botão de regularização imediata.
- **Canceled:** Aviso de encerramento de ciclo e perda de recursos Pro.

## 6. Integração Técnica
- **Endpoints:**
  - `POST /api/admin/billing/upgrade`
  - `POST /api/admin/billing/portal`
- **Webhooks:** Processa eventos `customer.subscription.updated` do Stripe.

---
![Billing Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-billing.png)
# 💳 AdminSettingsBillingPage
> **Plataforma:** WEB | **Domínio:** SAAS | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Gestão financeira da assinatura. Centraliza cobrança e controle de limites do plano.

## 2. Estrutura e Layout (Componentes)
- **Subscription Card:** Status e valor.
- **Usage Progress:** Barras de limite de pedidos.

## 3. Interações e Ações (Botões)
- **Upgrade Button:** Gatilho para Stripe.
- **Billing Portal:** Link externo de gestão.

## 4. Estados e Cenários (Loading/Error)
- **Active:** Assinatura em dia.
- **Past Due:** Alerta de atraso.

## 5. Fluxo de Navegação
1. Acesso via Configurações.
2. Seleção de plano.
3. Pagamento.

## 6. Documentação Técnica (API)
- **Endpoints:** `POST /api/admin/billing/upgrade`, `POST /api/admin/billing/portal`
- **Assets:** ![Billing Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/billing-full.png)
