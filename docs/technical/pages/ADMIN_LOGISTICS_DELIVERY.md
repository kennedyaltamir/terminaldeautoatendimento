# 🛵 Tela: Logística & Delivery
**Rota:** `/admin/[slug]/delivery`
**Domínio:** ADMIN / LOGISTICS

## 1. Especificação Visual
- **Fila de Entregas:** Cards de pedidos com status `ready` ou `delivering`.
- **Mapa de Entregadores:** (Se GPS ativo) Localização em tempo real dos motoboys.
- **Status de Frota:** Lista de entregadores logados e sua carga atual.

## 2. Elementos Interagíveis
- **Botão "Despachar":** Abre modal para selecionar o entregador e disparar o pedido.
- **Botão "Finalizar":** Baixa manual caso o entregador esqueça de confirmar no app.
- **Link WhatsApp:** Abre conversa direta com o cliente.

## 3. Comportamento Esperado
- **Notificação:** Ao despachar, disparar automaticamente o template de WhatsApp "Saiu para Entrega" com link de rastreio.
- **Cálculo de Dívida:** Se o pagamento for "Dinheiro", o valor do pedido deve ser debitado no `DriverLedger` do motoboy.

## 4. APIs Consumidas
- `GET /api/admin/delivery/orders`: Pedidos pendentes de entrega.
- `PATCH /api/admin/delivery/orders/{id}/dispatch`: Atribuição de motorista.
- `GET /api/admin/logistics/dashboard`: Métricas de tempo médio de entrega.
