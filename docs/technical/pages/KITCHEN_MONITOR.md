# 👨‍🍳 Tela: Monitor de Cozinha (KDS)
**Rota:** `/admin/[slug]/kitchen` (Web) | `OrdersScreen` (Mobile)
**Domínio:** ADMIN / OPERATION

## 1. Especificação Visual
- **Grid Dinâmico:** Cards de pedidos organizados por tempo de chegada.
- **Cores de SLA:**
    - **Verde:** < 10 min.
    - **Amarelo:** 10-20 min.
    - **Vermelho:** > 20 min (Atrasado).
- **Header:** Filtro de Estação (Cozinha/Bar) e Status da Conexão.

## 2. Elementos Interagíveis
- **Botão "Aceitar":** Move status de `pending` para `preparing`.
- **Botão "Pronto":** Move status para `ready` e dispara notificação para o cliente/garçom.
- **Botão "Recall":** (Backlog) Recupera o último pedido finalizado.
- **Item Individual:** Permite dar baixa em um item específico do pedido.

## 3. Comportamento Esperado
- **Alertas:** Tocar som "notification.mp3" a cada novo pedido.
- **Vibração:** No mobile, vibrar em ciclos de 500ms para pedidos que entram no estado "Vermelho".
- **Persistência:** Se a página for atualizada, o estado dos cronômetros deve ser mantido (calculado via `created_at`).

## 4. APIs Consumidas
- `GET /api/admin/{slug}/orders`: Lista inicial.
- `PATCH /api/admin/orders/{id}`: Atualização de status.
- `WS /ws/{slug}`: Recebimento de eventos `new_order`.
