# Changelog - MesaFlow

## [2.1.0] - 2026-01-02 - "Enterprise Polish"
Foco total em experiência do usuário (UX), resiliência e operações de cozinha.

### ✨ Novidades (Frontend)
- **Menu:** Navegação "Sticky" com Scroll Spy para categorias.
- **Menu:** Barra de busca em tempo real e filtros por Tags.
- **Menu:** Edição de itens diretamente no carrinho (quantidade/observações).
- **Menu:** Modal de "Dividir Conta" (Split Bill) com calculadora integrada.
- **Menu:** Indicador visual de status de conexão (Offline/Online).
- **Admin:** Editor de Mapa de Sala com Drag & Drop.

### 👨‍🍳 Melhorias Operacionais (KDS)
- **SLA Timer:** Cronômetro nos cards (Verde < 10min, Amarelo < 20min, Vermelho > 20min).
- **Recall:** Botão de histórico para restaurar pedidos finalizados acidentalmente.
- **Gestão Rápida (86):** Modal para bloquear/desbloquear produtos sem sair da tela da cozinha.
- **Impressão:** CSS `@media print` otimizado para impressoras térmicas (sem margens, fonte mono).

### 🛠️ Técnico (Backend & Infra)
- **WebSocket:** Implementada reconexão automática com *Exponential Backoff*.
- **Persistência:** Carrinho de compras agora persiste no `localStorage`.
- **Database:** Adicionados campos de posição (`position_x`, `position_y`) nas mesas.
- **Database:** Adicionado campo `tags` nos produtos.
- **API:** Novos endpoints para gestão rápida de estoque e histórico recente.

---

## [2.0.0] - 2025-12-31 - "MVP Híbrido"
Lançamento da versão base com suporte a Mesa e Delivery.
- Cardápio Digital via QR Code.
- KDS em Tempo Real.
- Gestão de Mesas e Comandas.



# Changelog - MesaFlow

## [2.2.0] - 2026-01-03 - "Fintech & Mobile Operations"
Atualização massiva focada na monetização da plataforma e na operação móvel dos garçons.

### 💰 Motor Financeiro (SaaS)
- **Split de Pagamento (Pix):** Implementada divisão automática de receita via Mercado Pago. O SaaS retém a comissão (`marketplace_fee_percentage`) na fonte.
- **Gestão de Assinaturas (Stripe):**
    - Integração completa com Stripe Checkout para upgrade de planos (Free -> Pro).
    - Portal do Cliente para gestão de cartões e cancelamento.
    - Webhooks para bloqueio/desbloqueio automático de recursos baseados no status do pagamento.
- **Dashboard Financeiro Real:**
    - Substituídos dados *mock* por agregações SQL nativas (`SUM`, `DATE_TRUNC`).
    - Gráficos de Faturamento, Ticket Médio e Vendas por Hora em tempo real.
- **Fidelidade (Cashback):**
    - Carteira digital (`CustomerWallet`) criada automaticamente pelo telefone do cliente.
    - Crédito automático de % do pedido após confirmação de pagamento.
    - Widget de saldo no carrinho para uso imediato dos pontos.

### 👨‍🍳 App do Garçom (Mobile POS)
- **Interface Mobile-First:** Redesign completo da rota `/waiter` para uso em celulares.
- **Módulo QuickPOS:**
    - **Venda Balcão:** Fluxo simplificado para pedidos sem mesa (Takeout).
    - **Novo Delivery:** Formulário rápido para lançar pedidos telefônicos.
- **Gestão de Mesas Avançada:**
    - **Transferência:** Mover comanda da Mesa X para Mesa Y.
    - **Merge:** Unificar comandas de mesas diferentes.
- **Notificações Sensoriais:**
    - Vibração e Som no celular do garçom quando a cozinha finaliza um prato ou o cliente chama.
- **Atalhos Rápidos:** Seção "Mais Vendidos" no topo do POS para lançamento ágil (ex: Água, Cerveja).

### 🛠️ Técnico
- **Testes de Integração:** Novos testes cobrindo o payload do Mercado Pago e o ciclo de vida do Stripe.
- **Refatoração de API:** Otimização dos endpoints de métricas para performance em escala.