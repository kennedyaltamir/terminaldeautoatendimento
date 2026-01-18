# 🔌 Especificação Técnica: TASK-INT-01
> **Título:** Documentação e Setup de Integrações (Google, Stripe, MP, iFood)
> **Status:** SPECIFIED

## 1. Objetivo
Consolidar o guia de configuração para as quatro integrações pilares do ecossistema MesaFlow, garantindo que o lojista consiga ativar os serviços de forma autônoma.

## 2. Escopo de Configuração
### 2.1. Google OAuth
- Criação do projeto no Google Cloud Console.
- Configuração da tela de consentimento e URIs de redirecionamento.
- Obtenção do `GOOGLE_CLIENT_ID`.

### 2.2. Stripe (SaaS Billing)
- Configuração de Webhooks para `checkout.session.completed`.
- Definição do `STRIPE_PRO_PRICE_ID` para assinaturas recorrentes.

### 2.3. Mercado Pago (Fintech Split)
- Ativação do modo Marketplace/Agregador.
- Configuração do `MP_REDIRECT_URI` para o fluxo OAuth de vendedores.

### 2.4. iFood (Marketplace Sync)
- Setup do `IFOOD_WEBHOOK_SECRET` para recepção de pedidos.
- Mapeamento de SKUs (external_id).

## 3. Requisitos Técnicos
- Atualização do manual `docs/technical/INTEGRATION_HUB_GUIDE.md`.
- Criação de placeholders seguros no `.env.example`.
