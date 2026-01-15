# 🧠 MesaFlow AI Knowledge Base
**Status:** ACTIVE | **Maturity:** L8.7

--- ENTRY: 2026-01-15T15:45:00 ---
**CONTEXT:** L8.7 Driver UI Stabilization.
**DECISION:** Implementado `lastActiveOrder` no `DriverPage` para manter a renderização do painel de entrega mesmo durante gaps de sincronia do polling. Adicionado `data-testid="driver.delivery.finish-btn"` para eliminar ambiguidades de seletor no Playwright.
**LEARNING:** Em sistemas distribuídos, o estado local da UI deve ser "pegajoso" (sticky). Se o usuário iniciou uma ação (pickup), a UI deve sustentar esse estado até uma confirmação explícita de término, protegendo o operador contra flutuações da lista de pedidos do servidor.
**STATUS:** Fluxo de finalização blindado.
