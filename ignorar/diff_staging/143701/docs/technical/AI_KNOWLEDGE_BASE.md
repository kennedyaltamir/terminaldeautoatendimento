# 🧠 MesaFlow AI Knowledge Base
**Status:** ACTIVE | **Maturity:** L9.0

--- ENTRY: 2026-01-15T14:35:00 ---
**CONTEXT:** Systemic Event Mismatch (Backend vs Client).
**DECISION:** Implementação de um **Event Adapter** no Backend (`admin_delivery.py`). O sistema agora emite eventos redundantes: `delivery.status` (técnico) e `order_update` (domínio).
**LEARNING:** Em arquiteturas multi-persona, a nomenclatura de eventos deve ser agnóstica ao emissor e focada no consumidor. O Frontend do Cliente não deve conhecer detalhes de "delivery", apenas mudanças no estado do seu "order".
**STATUS:** Sincronia restaurada. Mapa do cliente agora reage instantaneamente ao despacho.
