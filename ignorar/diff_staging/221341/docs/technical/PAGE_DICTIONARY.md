# 📖 Dicionário de Páginas e Comportamentos (Sovereign Edition)
**Versão:** 10.0 — SSOT Final
**Objetivo:** Mapear a intenção de negócio, elementos e APIs de cada rota para eliminar o retrabalho.

---

## 1. Contexto Público (Cliente Final)

| Rota | Nome | Intenção de Negócio | Comportamento Esperado | APIs / Sockets |
| :--- | :--- | :--- | :--- | :--- |
| `/` | **Landing Page** | Venda SaaS e captura de leads. | Scroll-reveal, ROI Calc. | `POST /api/leads` |
| `/[slug]/menu` | **Cardápio Digital** | Interface principal de venda. | Offline-first, Carrinho local. | `GET /menu`, `POST /orders` |
| `/[slug]/kiosk` | **Totem** | Autoatendimento físico. | Passivo. Reseta após 60s. | - |
| `/[slug]/monitor` | **Monitor** | Senhas de retirada. | Read-only. Atualiza via WS. | `WS /ws/[slug]` |
| `/trust` | **Trust Center** | Transparência técnica. | Exibe Uptime e Segurança. | `GET /health` |
| `/offline` | **Offline** | Resiliência de rede. | Fallback visual. Auto-ping. | - |

## 2. Contexto Administrativo (Gestão)

| Rota | Nome | Intenção | Comportamento | APIs |
| :--- | :--- | :--- | :--- | :--- |
| `/admin/login` | **Acesso** | Entrada segura. | JWT Storage, Role Redirect. | `POST /auth/token` |
| `/admin/register` | **Cadastro** | Onboarding SaaS. | Multi-step, Auto-seed. | `POST /auth/register` |
| `.../dashboard` | **BI** | Visão Geral. | Gráficos Recharts, KPIs. | `GET /metrics` |
| `.../menu` | **Menu Admin** | Gestão de Itens. | ImageUpload, Cache Inval. | `GET /menu/products` |
| `.../inventory` | **Estoque** | Insumos. | Alerta Crítico, Ficha Técnica. | `GET /inventory` |
| `.../tables` | **Mesas** | Salão. | Drag & Drop, QR Generator. | `GET /tables` |
| `.../audit/financial`| **Ledger** | Transparência. | Read-only, Hash Chain. | `GET /audit/financial` |
| `.../settings/billing`| **Faturamento** | SaaS. | Stripe Portal, Plan Cards. | `POST /billing/upgrade` |

## 3. Contexto Operacional (Staff)

| Rota / Tela | Nome | Intenção | Comportamento | APIs / Hardware |
| :--- | :--- | :--- | :--- | :--- |
| `.../kitchen` | **KDS Web** | Produção. | WebSocket `new_order`, Som. | `PATCH /orders/{id}` |
| `OrdersScreen` | **KDS Mobile** | Produção. | FlashList, Vibração. | `WS`, `Vibration` |
| `WaiterTables` | **POS Mapa** | Atendimento. | Grid de mesas, Long-press. | `GET /tables` |
| `OrderEntry` | **Lançamento** | Venda Mesa. | QuickSearch, Fila Offline. | `POST /orders` |
| `DriverDash` | **Logística** | Entrega. | GPS Tracking, POD Code. | `PATCH /dispatch` |
| `PrinterDebug` | **Suporte** | Hardware. | Teste de Buffer ESC/POS. | `Bluetooth` |

---
*Nota: Para especificações detalhadas de cada elemento, consulte `docs/technical/pages/*.md`.*
