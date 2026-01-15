# 🧠 MesaFlow AI Knowledge Base
**Status:** ACTIVE | **Maturity:** L8.1

--- ENTRY: 2026-01-15T15:10:00 ---
**CONTEXT:** L8 Simulation Failure (Map Visibility).
**DECISION:** Injeção mandatória de telemetria GPS inicial antes da asserção de visibilidade do mapa.
**LEARNING:** A UI do cliente no MesaFlow OS utiliza renderização condicional baseada em dados de telemetria (`driverPos`). O status `delivering` sozinho não garante a montagem do componente de mapa no DOM; é necessário um evento de localização para disparar o estado interno do componente `OrderStatusView`.
**STATUS:** Script `enterprise_delivery_l8.py` corrigido e estabilizado.
