# 📱 Telas: Variantes do POS (Garçom)
**Rotas:** `/admin/[slug]/waiter/pos/quick` | `/admin/[slug]/waiter/pos/[tableId]`

## 1. POS Rápido (Quick POS)
- **Intenção:** Vendas diretas sem vínculo com mesa (ex: balcão ou fila).
- **Comportamento:** Pula a seleção de mesa e vai direto para o carrinho. O status do pedido nasce como `delivered`.

## 2. POS de Mesa (Table POS)
- **Intenção:** Atendimento tradicional de salão.
- **Comportamento:** Vincula o pedido ao `table_id` e `session_id`. Permite adicionar itens a uma conta já aberta.

## 3. APIs Consumidas
- `POST /api/admin/orders`: Criação de pedido com contexto de staff.
