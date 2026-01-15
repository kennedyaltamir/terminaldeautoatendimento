# 🖥️ Tela: Dashboard Administrativo (BI)
**Rota:** `/admin/[slug]/dashboard`
**Domínio:** ADMIN / MANAGEMENT

## 1. Especificação Visual
- **KPI Cards:** Faturamento Total, Ticket Médio, Total de Pedidos, Novos Clientes.
- **Gráficos:** Evolução de vendas (Área), Vendas por Hora (Barras), Top 5 Produtos (Pizza).
- **Filtros:** Seletor de período (Hoje, 7 dias, 30 dias, Custom).

## 2. Elementos Interagíveis
- **Botão "Exportar CSV":** Dispara download de relatório contábil.
- **Toggle de Período:** Dispara re-fetch nas métricas.
- **Cards de Produto:** Clique leva para a edição do produto no menu.

## 3. Comportamento Esperado
- **Real-time:** Os números de "Hoje" devem atualizar automaticamente via WebSocket quando um pedido é pago.
- **Segurança:** Apenas usuários com role `owner` ou `manager` podem visualizar dados financeiros.
- **Skeleton:** Exibir pulse animation enquanto os dados de agregação (SQL sum/count) são processados.

## 4. APIs Consumidas
- `GET /api/admin/metrics`: Dados agregados para os gráficos.
- `GET /api/admin/metrics/export`: Stream de arquivo CSV.
