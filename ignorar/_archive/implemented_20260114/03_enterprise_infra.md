# 🏢 Enterprise & Infraestrutura

## 1. Arquitetura Multi-tenant
- **Estratégia:** Isolamento Lógico (Row-Level).
- **Segurança:** Todas as queries filtram obrigatoriamente por `company_id`.
- **White Label:** Suporte a domínios personalizados (`custom_domain`) resolvidos via Middleware.

## 2. Cache L2 (Redis)
- **Objetivo:** Proteger o banco de dados em horários de pico.
- **Implementação:** Decorator `@cache_response` nas rotas públicas.
- **Invalidação:** Automática (Hooks) ao criar/editar/deletar produtos ou categorias.

## 3. Marketing & IA
- **Motor de Recomendação:**
    - Analisa histórico de pedidos (`order_items`).
    - Calcula co-ocorrência (Quem comprou A também comprou B).
    - Gera sugestões de Upsell no carrinho.
- **Automação:** Disparo de mensagens WhatsApp (API Evolution) para status de pedido.

## 4. Gestão de Franquias
- **Visão Consolidada:** Dashboard que agrega faturamento de todas as lojas de um mesmo dono (`owner_email`).
- **Ranking:** Comparativo de performance entre unidades.

## 5. Segurança (Hardening)
- **Rate Limiting:** `SlowAPI` configurado em rotas críticas (Login, Pedidos).
- **Sanitização:** Filtro de XSS em todos os inputs de texto.
- **Auditoria:** Logs imutáveis (`audit_logs`) para ações sensíveis.
