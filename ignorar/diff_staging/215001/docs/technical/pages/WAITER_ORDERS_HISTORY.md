# 📱 Tela: Histórico do Garçom
**Rota:** `/admin/[slug]/waiter/orders`
**Domínio:** MOBILE / OPERATION

## 1. Especificação Visual
- **Lista Cronológica:** Pedidos realizados pelo garçom logado no turno atual.
- **Status Visual:** Cards compactos com ID, Mesa e Valor.

## 2. Elementos Interagíveis
- **Botão "Reimprimir":** Dispara nova via para a impressora Bluetooth.
- **Filtro de Status:** Ver apenas pedidos "Prontos" ou "Em Preparo".

## 3. Comportamento Esperado
- **Performance:** Carregamento via cache local (Zustand) com re-fetch em background.
- **Segurança:** O garçom só vê os pedidos que ele mesmo lançou ou pedidos da sua praça atribuída.

## 4. APIs Consumidas
- `GET /api/admin/[slug]/history?waiter_id=X`: Lista filtrada.
