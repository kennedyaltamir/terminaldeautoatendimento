# 📊 Tela: Histórico de Dashboard (Drill-down)
**Rota:** `/admin/[slug]/dashboard/history`
**Domínio:** ADMIN / BI

## 1. Especificação Visual
- **Gráficos de Tendência:** Comparativo de performance entre períodos (ex: Esta semana vs Semana passada).
- **Tabela de Performance:** Lista de produtos com maior margem de lucro e volume de vendas.

## 2. Elementos Interagíveis
- **Seletor de Métrica:** Alternar entre Receita, Volume de Pedidos e Ticket Médio.
- **Botão "Ver Detalhes do Produto":** Redireciona para a ficha técnica no estoque.

## 3. Comportamento Esperado
- **Agregação Dinâmica:** Os dados devem ser recalculados via SQL `GROUP BY` conforme o filtro de data.
- **Exportação:** Permite baixar o recorte específico do gráfico em formato PNG ou CSV.

## 4. APIs Consumidas
- `GET /api/admin/metrics/history`: Dados históricos agregados.
