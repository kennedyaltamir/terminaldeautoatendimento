# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:15:00
# 🖥️ DashboardPage
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/admin/[slug]/dashboard`
> **Acesso:** Protected (Owner/Manager)
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Visão tática da operação em tempo real. Apresenta KPIs financeiros, operacionais e alertas de sistema.
**Persona Principal:** Dono, Gerente.

## 2. Estrutura de Interface
- **Layout Pai:** `AdminLayout` (Com Sidebar e Header).
- **Componentes Chave:**
  - `KPICards`: Cards de Faturamento, Ticket Médio, Pedidos.
  - `SalesChart`: Gráfico de área (Recharts) com evolução diária.
  - `RecentOrders`: Tabela simplificada dos últimos pedidos.

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `Filtro Data` | Dropdown | `setPeriod` | Skeleton Loading | Refetch Metrics |
| `Exportar` | Button | `handleExport` | Toast "Baixando..." | Download CSV |
| `Ver Todos` | Link | Navegação | Hover effect | Vai para `/history` |

## 4. Estados da Tela
- **Loading:** Skeletons animados nos Cards e Gráfico.
- **Empty:** "Nenhum dado no período" (Gráfico zerado).
- **Error:** Toast "Falha ao carregar métricas".

## 5. Fluxos de Navegação
1. **Entrada:** Login ou Menu Lateral.
2. **Saída (Drill-down):** Clicar em um pedido leva ao detalhe do pedido.

## 6. Regras de Negócio Críticas
- [x] Dados financeiros devem ser exibidos em Reais (BRL).
- [x] Filtro padrão deve ser "Hoje".
- [x] Acesso restrito a roles `owner` e `manager`.

## 7. Dados & Integração
- **API Endpoints:**
  - `GET /api/admin/metrics?start_date=...&end_date=...`

