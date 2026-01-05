# 💰 Financeiro & SaaS

## 1. Split de Pagamento (Marketplace)
- **Provedor:** Mercado Pago (OAuth).
- **Fluxo:**
    1. Cliente paga via Pix (QR Code Dinâmico).
    2. Webhook confirma pagamento.
    3. Mercado Pago divide o valor na fonte:
        - `marketplace_fee_percentage` -> Conta do MesaFlow.
        - Restante -> Conta do Restaurante.
- **Status:** Implementado e testado com Mock e Integração Real.

## 2. Gestão de Assinaturas (SaaS)
- **Provedor:** Stripe.
- **Planos:**
    - **Free:** Limite de 15 produtos, 50 pedidos/mês.
    - **Pro:** Ilimitado + KDS + Estoque.
- **Automação:**
    - Webhooks do Stripe atualizam o `plan_tier` da empresa automaticamente.
    - Portal do Cliente para gestão de cartão/cancelamento.

## 3. Fidelidade (Cashback)
- **Lógica:**
    - Carteira vinculada ao telefone do cliente.
    - Acúmulo: % do valor pago (configurável por loja).
    - Resgate: Desconto automático no próximo pedido.
- **Persistência:** Tabela `customer_wallets`.

## 4. Dashboard Financeiro
- **Métricas:**
    - Faturamento Bruto.
    - Ticket Médio.
    - Vendas por Hora (Heatmap).
    - Curva ABC de Produtos.
- **Tecnologia:** Agregações SQL (SQLAlchemy `func.sum`, `func.count`) para performance.
