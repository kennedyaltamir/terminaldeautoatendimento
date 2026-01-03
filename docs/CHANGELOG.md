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