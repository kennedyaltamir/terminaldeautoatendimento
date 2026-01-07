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

# Changelog - MesaFlow

## [2.3.2] - 2026-01-05 - "CI/CD Stabilization"
Foco na confiabilidade da infraestrutura de testes e automação de deploy.

### 🛠️ Engenharia & DevOps
- **Pipeline CI/CD:** Correção de 29 erros na suíte de testes (`pytest`).
- **Database Testing:** Implementação de `GUID` híbrido para compatibilidade total entre SQLite (Testes) e PostgreSQL (Produção).
- **Mocking Strategy:** Refatoração dos testes de integração (Redis/HTTPX) para suportar chamadas assíncronas complexas.
- **Hardening:** Correção de rotas administrativas e validação de payloads financeiros.

---

## [2.2.0] - 2026-01-03 - "Fintech & Mobile Operations"
Atualização massiva focada na monetização da plataforma e na operação móvel dos garçons.

### 💰 Motor Financeiro (SaaS)
- **Split de Pagamento (Pix):** Implementada divisão automática de receita via Mercado Pago.
- **Gestão de Assinaturas (Stripe):** Integração completa com Checkout e Portal do Cliente.
- **Dashboard Financeiro Real:** Métricas SQL nativas.

### 👨‍🍳 App do Garçom (Mobile POS)
- **Interface Mobile-First:** Redesign completo da rota `/waiter`.
- **Módulo QuickPOS:** Venda Balcão e Novo Delivery.
- **Gestão de Mesas:** Transferência e Merge de comandas.

---

## [2.1.0] - 2026-01-02 - "Enterprise Polish"
Foco total em experiência do usuário (UX), resiliência e operações de cozinha.

### ✨ Novidades (Frontend)
- **Menu:** Navegação "Sticky" e Busca em tempo real.
- **KDS:** SLA Timer e Recall de pedidos.
- **Infra:** WebSocket com reconexão automática.

---

## [2.0.0] - 2025-12-31 - "MVP Híbrido"
Lançamento da versão base com suporte a Mesa e Delivery.
# 📝 Changelog - MesaFlow

## [3.0.0] - 2026-01-05 - "The Enterprise Milestone"
Esta versão marca a transição do MesaFlow de um software de gestão para uma plataforma de integração e resiliência.

### ✨ Novidades (Fase 9)
- **Contingência Fiscal:** Emissão de notas em modo offline com sincronização automática via IndexedDB.
- **Hub iFood:** Integração nativa com iFood. Pedidos externos agora caem direto no KDS do MesaFlow.
- **Webhooks de Saída:** Sistema de notificações para desenvolvedores com assinatura HMAC-SHA256.
- **Motor de Promoções:** Criação e validação de cupons de desconto (fixo/percentual) com regras de valor mínimo.
- **Developer Experience:** Documentação técnica completa via Swagger (/docs) e Redoc (/redoc).

### 🛠️ Melhorias Técnicas
- **Integridade:** Migração total de lógica financeira para o tipo `Decimal`.
- **Segurança:** Implementação de GUIDs (UUID v4) em todas as tabelas para compatibilidade SQLite/Postgres.
- **KDS:** Suporte visual para pedidos iFood e atalhos de teclado (Bump Bar).
- **Infra:** Otimização do loop de eventos do FastAPI para suportar polling de múltiplos merchants iFood.

---

## [2.3.2] - 2026-01-05 - "CI/CD Stabilization"
- Correção de 29 regressões na suíte de testes.
- Implementação de GUID híbrido.

---
# 📝 Changelog - MesaFlow

## [4.0.0] - 2026-01-07 - "The Mobile Revolution"
Esta versão consolida a entrada do MesaFlow no ecossistema nativo com o lançamento do KDS Mobile.

### ✨ Novidades (Fase 10)
- **KDS Nativo:** Aplicativo de alta performance para tablets e celulares.
- **Active Attention:** Sistema de alertas sensoriais (vibração) inteligente com controle de SLA.
- **Global Clock:** Sincronização temporal determinística em todo o app.
- **Resiliência Total:** Reconexão automática de WebSocket e persistência local de pedidos.
- **Observabilidade:** Logs estruturados para diagnóstico em tempo real.

### 🛠️ Melhorias Técnicas
- **Auth Hardening:** Validação semântica de JWT e barreira de renderização soberana.
- **Zustand Persistence:** Estado operacional salvo no dispositivo (Offline-ready).
- **API Contracts:** Padronização de esquemas de erro para clientes nativos.

---
