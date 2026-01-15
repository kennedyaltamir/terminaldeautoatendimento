# 💳 Tela: Configurações & Faturamento (SaaS)
**Rota:** `/admin/[slug]/settings/billing`
**Domínio:** ADMIN / SAAS

## 1. Especificação Visual
- **Plan Cards:** Comparativo Free vs Pro vs Enterprise.
- **Status de Assinatura:** Data de renovação, status do cartão, faturas pendentes.
- **Configuração de Taxas:** Definição de % de comissão de garçom e taxa de entrega fixa.

## 2. Elementos Interagíveis
- **Botão "Upgrade para Pro":** Redireciona para o Stripe Checkout.
- **Botão "Portal do Cliente":** Abre o Stripe Billing Portal para gerenciar cartões.
- **Input "Taxa de Serviço":** Define o multiplicador global para o POS.

## 3. Comportamento Esperado
- **Paywall:** Se o plano for `free`, desabilitar funcionalidades como KDS e Gestão de Estoque com um aviso de upgrade.
- **Sincronia:** Mudanças no Stripe (cancelamento) devem refletir no `plan_tier` do banco via Webhook em < 5s.

## 4. APIs Consumidas
- `GET /api/admin/company/me`: Dados atuais da empresa.
- `POST /api/admin/billing/upgrade`: Gera URL de checkout.
- `POST /api/admin/billing/portal`: Gera URL de gestão.
