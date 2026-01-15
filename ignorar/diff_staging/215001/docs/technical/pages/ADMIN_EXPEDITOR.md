# 📦 Tela: Expedição & Montagem
**Rota:** `/admin/[slug]/expeditor`
**Domínio:** ADMIN / OPERATION

## 1. Especificação Visual
- **Checklist de Itens:** Lista de todos os produtos de um pedido com checkbox de conferência.
- **Timer de Saída:** Tempo decorrido desde que a cozinha marcou como "Pronto".

## 2. Elementos Interagíveis
- **Checkbox de Item:** Marca que o item foi colocado na bandeja/embalagem.
- **Botão "Despachar":** Finaliza o ciclo e notifica o cliente/entregador.

## 3. Comportamento Esperado
- **Integridade:** O botão "Despachar" só habilita se todos os itens obrigatórios forem conferidos.
- **Notificação:** Dispara evento `order_dispatched` via WebSocket.

## 4. APIs Consumidas
- `GET /api/admin/[slug]/orders?status=ready`: Pedidos aguardando montagem.
- `PATCH /api/admin/orders/{id}/dispatch`: Finalização da expedição.
