# 💰 Especificação Técnica: TASK-FIN-03
> **Título:** Validação do Fluxo de Split (2.5%) e Mensalidade
> **Status:** SPECIFIED

## 1. Regras de Negócio (Fintech)
O MesaFlow deve garantir a sustentabilidade do modelo SaaS através de duas fontes de receita:

### 1.1. Split Transacional (Take Rate)
- **Taxa:** 2.5% sobre o valor bruto de cada pedido pago via Pix/Cartão no QR Code.
- **Mecanismo:** O `PaymentService` deve injetar a `application_fee` na chamada da API do Mercado Pago.
- **Arredondamento:** Sempre para baixo (floor) em centavos.

### 1.2. Mensalidade (Subscription)
- **Valor:** R$ 149,00/mês (Plano Pro).
- **Gatilho:** Cobrança via Stripe.
- **Inadimplência:** Se o webhook do Stripe reportar `past_due`, o sistema deve bloquear o acesso ao KDS e Mobile POS em 72h.

## 2. Requisitos Técnicos
- Refatoração do `app/services/payment_service.py` para tornar a taxa configurável por tenant (default 2.5%).
- Implementação de trava de segurança: o split não pode ser aplicado se o valor resultante for < R$ 0,01.
