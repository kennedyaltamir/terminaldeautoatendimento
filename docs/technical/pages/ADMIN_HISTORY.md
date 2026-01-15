# 📜 Tela: Histórico de Vendas
**Rotas:** `/admin/[slug]/history` | `/admin/[slug]/dashboard/history`

## 1. Especificação Visual
- **Tabela Mestre:** Lista exaustiva de todos os pedidos (ID, Cliente, Mesa, Total, Status, Pagamento).
- **Badges de Status:** Cores padronizadas (Verde=Pago, Vermelho=Cancelado).

## 2. Elementos Interagíveis
- **Botão "Ver Comanda":** Abre o detalhe dos itens consumidos.
- **Botão "Emitir Nota":** Atalho para o módulo fiscal caso a nota não tenha sido gerada.
- **Filtro Avançado:** Busca por telefone do cliente ou ID da transação.

## 3. Comportamento Esperado
- **Auditoria:** Exibe o `external_id` do gateway para facilitar a conferência bancária.
- **Paging:** Suporte a milhares de registros via cursor-based pagination.

## 4. APIs Consumidas
- `GET /api/admin/[slug]/history`: Lista paginada.

