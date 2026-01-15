# 🗺️ Roadmap de Integrações Enterprise

Este documento mapeia as configurações pendentes para o fechamento do ciclo de produção.

## 1. Mercado Pago (Prioridade: ALTA)
- **Função:** Recebimento de Pix e Cartão no PDV e Mobile.
- **Status:** Código implementado, aguardando credenciais reais.
- **Ação:** Criar aplicação no [Mercado Pago Developers](https://www.mercadopago.com.br/developers/).

## 2. Stripe (Prioridade: MÉDIA)
- **Função:** Gestão de assinaturas do SaaS MesaFlow.
- **Status:** `StripeService` funcional, aguardando IDs de produtos reais.
- **Ação:** Configurar Dashboard Stripe e Webhooks.

## 3. WhatsApp / Evolution API (Prioridade: ALTA)
- **Função:** Notificar cliente (Pedido Pronto) e Staff (Estoque Baixo).
- **Status:** `WhatsAppService` aguardando instância ativa.
- **Ação:** Provisionar servidor Evolution API ou conectar via Twilio.

## 4. iFood Hub (Prioridade: BAIXA)
- **Função:** Centralizar pedidos do iFood no KDS do MesaFlow.
- **Status:** Lógica de ingestão pendente de homologação com a API do iFood.
- **Ação:** Solicitar acesso de desenvolvedor no portal iFood.

---
*Gerado por MesaFlow Kernel L6 — 2026-01-15*
