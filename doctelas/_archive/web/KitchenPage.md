# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:15:00
# 🖥️ KitchenPage (KDS)
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/admin/[slug]/kitchen`
> **Acesso:** Protected (Kitchen/Manager/Owner)
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Sistema de Exibição de Cozinha (KDS). Substitui impressoras de papel, organizando pedidos por prioridade e tempo de espera.
**Persona Principal:** Cozinheiro, Chefe de Cozinha.

## 2. Estrutura de Interface
- **Layout Pai:** `AdminLayout` (Modo Focado/Fullscreen recomendado).
- **Componentes Chave:**
  - `OrderCard`: Card individual do pedido com itens e timer.
  - `StationFilter`: Filtro por praça (Cozinha/Bar/Sobremesa).
  - `Aggregator`: Resumo de itens a produzir (ex: "5x X-Bacon").

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `Avançar Status` | Button | `handleAdvance` | Card some/move | `PATCH /api/orders` |
| `Filtro Praça` | Tabs | `setStation` | Lista filtra | Local Filter |
| `Resumo` | Toggle | `toggleAggregator` | Modal lateral | - |

## 4. Estados da Tela
- **Real-time:** Atualização via WebSocket (`new_order`, `order_update`).
- **SLA Warning:** Cards ficam amarelos/vermelhos conforme o tempo passa.
- **Empty:** "Cozinha Livre" (Ilustração).

## 5. Fluxos de Navegação
1. **Entrada:** Menu Lateral -> Produção.
2. **Fluxo:** Pedido Pendente -> Preparando -> Pronto (Sai da tela ou vai para Expedição).

## 6. Regras de Negócio Críticas
- [x] Deve emitir som ao chegar novo pedido.
- [x] Não deve permitir pular status (Pendente -> Pronto) sem passar por Preparando (configurável).
- [x] Deve persistir filtro de praça no LocalStorage.

## 7. Dados & Integração
- **API Endpoints:**
  - `GET /api/admin/[slug]/orders`
  - `PATCH /api/admin/orders/[id]`
- **WebSocket:** Canal `mesaflow:[slug]`.

