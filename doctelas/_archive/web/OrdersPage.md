# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:15:00
# 🖥️ OrdersPage (Gestão de Pedidos)
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/admin/[slug]/waiter/orders`
> **Acesso:** Protected (Waiter/Cashier/Manager)
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Visão tabular de todos os pedidos ativos e recentes para gestão de salão e caixa. Permite cancelamento e reimpressão.
**Persona Principal:** Garçom, Caixa.

## 2. Estrutura de Interface
- **Layout Pai:** `AdminLayout`.
- **Componentes Chave:**
  - `OrdersTable`: Tabela com colunas ordenáveis (Mesa, Cliente, Status, Total).
  - `StatusBadge`: Indicador visual do estado do pedido.
  - `ActionMenu`: Dropdown com ações (Cancelar, Imprimir, Detalhes).

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `Ver Detalhes` | Button | `openModal` | Modal abre | Fetch Details |
| `Cancelar` | Button | `handleCancel` | Prompt confirmação | `PATCH status=canceled` |
| `Imprimir` | Button | `handlePrint` | Janela de impressão | - |

## 4. Estados da Tela
- **Loading:** Skeleton nas linhas da tabela.
- **Empty:** "Nenhum pedido encontrado".
- **Pagination:** Controles de Próximo/Anterior.

## 5. Fluxos de Navegação
1. **Entrada:** Menu Lateral -> Pedidos.
2. **Drill-down:** Clicar na linha abre modal de detalhes.

## 6. Regras de Negócio Críticas
- [x] Pedidos "Entregues" não podem ser cancelados (apenas estornados por gerente).
- [x] Visualização deve respeitar permissões (Garçom vê seus pedidos ou todos, conforme config).

## 7. Dados & Integração
- **API Endpoints:**
  - `GET /api/admin/[slug]/history` (com filtros de status ativo)

